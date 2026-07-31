import tempfile
import unittest
from pathlib import Path

from scripts.build_site import build_article_html, build_summary_parts, reset_articles_output
from scripts.check_sensitive_data import is_text_file, scan_file
from scripts.kb import ARTICLE_ID_RE, html_escape, load_site_config, markdown_to_html
from scripts.new_article import load_retired_ids, next_article_id, slugify


class KbHelpersTest(unittest.TestCase):
    def test_article_id_pattern(self):
        self.assertTrue(ARTICLE_ID_RE.match("KB-2026-0001"))
        self.assertFalse(ARTICLE_ID_RE.match("kb-2026-1"))

    def test_html_escape_script(self):
        raw = '<script>alert("xss")</script>'
        escaped = html_escape(raw)
        self.assertNotIn("<script>", escaped)
        self.assertIn("&lt;script&gt;", escaped)

    def test_markdown_renders_heading(self):
        html = markdown_to_html("# Hello")
        self.assertIn("<h1>", html)

    def test_markdown_strips_script_element(self):
        html = markdown_to_html('<script>alert("xss")</script>')
        self.assertNotIn("<script", html.lower())

    def test_slugify(self):
        self.assertEqual(slugify("Hello World"), "hello-world")


class NewArticleIdTest(unittest.TestCase):
    def test_retired_ids_file_is_valid(self):
        retired = load_retired_ids()
        self.assertIsInstance(retired, set)
        for article_id in retired:
            self.assertTrue(ARTICLE_ID_RE.match(article_id))

    def test_next_id_starts_from_one_when_empty(self):
        nxt = next_article_id("2026")
        self.assertTrue(ARTICLE_ID_RE.match(nxt))
        self.assertNotIn(nxt, load_retired_ids())
        # After initial reset with no live articles, expect KB-2026-0001.
        # If live/retired IDs exist, next ID must still be unused.
        from scripts.kb import iter_article_dirs, load_article

        used = {load_article(d)["id"] for d in iter_article_dirs()} | load_retired_ids()
        if not used:
            self.assertEqual(nxt, "KB-2026-0001")
        else:
            self.assertNotIn(nxt, used)


class GeneratedOutputTest(unittest.TestCase):
    def test_reset_articles_output_removes_stale_pages(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "articles"
            stale = output / "2026" / "kb-2026-9999-stale" / "index.html"
            stale.parent.mkdir(parents=True)
            stale.write_text("stale", encoding="utf-8")

            reset_articles_output(output)

            self.assertTrue(output.is_dir())
            self.assertFalse(stale.exists())
            self.assertEqual([p.name for p in output.iterdir()], [".gitkeep"])


class SummaryDocumentTest(unittest.TestCase):
    def test_build_summary_parts_adds_toc_and_section_ids(self):
        md = "# Title\n\n## First\n\nBody\n\n## Second\n\nMore"
        toc_html, body_html = build_summary_parts(md)
        self.assertIn('href="#section-1"', toc_html)
        self.assertIn("First", toc_html)
        self.assertIn('id="section-1"', body_html)
        self.assertIn('id="section-2"', body_html)


class GiscusConfigurationTest(unittest.TestCase):
    def test_live_giscus_configuration_is_embedded_in_rendered_html(self):
        config = load_site_config()
        giscus = config["giscus"]

        self.assertTrue(giscus["enabled"])
        self.assertEqual(giscus["repo"], config["repositoryPath"])
        self.assertTrue(giscus["repoId"].startswith("R_"))
        self.assertEqual(giscus["category"], "Announcements")
        self.assertTrue(giscus["categoryId"].startswith("DIC_"))
        self.assertEqual(giscus["mapping"], "specific")
        self.assertEqual(giscus["strict"], "1")

        with tempfile.TemporaryDirectory() as tmp:
            article_dir = Path(tmp)
            (article_dir / "responses").mkdir()
            (article_dir / "article.json").write_text("{}", encoding="utf-8")
            (article_dir / "conclusion.md").write_text("# 結論\n", encoding="utf-8")
            (article_dir / "analysis.md").write_text("# 考察\n", encoding="utf-8")
            (article_dir / "prompt.txt").write_text("prompt\n", encoding="utf-8")
            (article_dir / "responses" / "chatgpt.md").write_text("# ok\n", encoding="utf-8")

            meta = {
                "schemaVersion": 1,
                "id": "KB-2099-0001",
                "slug": "fixture",
                "title": "giscus fixture",
                "description": "temporary fixture",
                "status": "draft",
                "publishedAt": None,
                "updatedAt": "2026-07-30",
                "lastVerifiedAt": "2026-07-30",
                "tags": ["fixture"],
                "agents": [
                    {
                        "name": "ChatGPT",
                        "model": "test",
                        "responseFile": "responses/chatgpt.md",
                        "executedAt": "2026-07-30",
                        "webSearch": False,
                        "attachmentsUsed": False,
                        "integrity": "raw",
                        "notes": None,
                    }
                ],
                "giscusTerm": "KB-2099-0001",
                "supersededBy": None,
                "_dir": article_dir,
                "_year": "2099",
                "_url": "/articles/2099/kb-2099-0001-fixture/",
                "_dirname": "kb-2099-0001-fixture",
            }
            html = build_article_html(meta, config)

        self.assertIn(f'data-repo="{giscus["repo"]}"', html)
        self.assertIn(f'data-repo-id="{giscus["repoId"]}"', html)
        self.assertIn(f'data-category-id="{giscus["categoryId"]}"', html)
        self.assertIn('data-mapping="specific"', html)
        self.assertIn('data-term="KB-2099-0001"', html)
        self.assertIn('data-strict="1"', html)


class SensitiveScanTest(unittest.TestCase):
    def test_detects_private_key_without_returning_value(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "leak.txt"
            path.write_text("-----BEGIN " + "PRIVATE KEY-----\nABC\n", encoding="utf-8")
            findings = scan_file(path, "leak.txt")
            kinds = [k for _, k, _ in findings]
            self.assertIn("private_key", kinds)
            self.assertTrue(all(snippet == "[MATCH_REDACTED]" for _, _, snippet in findings))

    def test_allows_redacted_placeholder(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ok.txt"
            path.write_text("token=[REDACTED_API_KEY]\n", encoding="utf-8")
            findings = scan_file(path, "ok.txt")
            self.assertEqual(findings, [])

    def test_redacted_placeholder_does_not_suppress_real_secret(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "leak.txt"
            key_name = "api_" + "key"
            secret_value = "actual-" + "secret-value"
            path.write_text(
                f'{key_name}="{secret_value}" [REDACTED_API_KEY]\n',
                encoding="utf-8",
            )
            findings = scan_file(path, "leak.txt")
            kinds = [k for _, k, _ in findings]
            self.assertIn("api_key_assignment", kinds)

    def test_safe_email_domain_requires_exact_domain(self):
        with tempfile.TemporaryDirectory() as tmp:
            safe_path = Path(tmp) / "safe.txt"
            safe_path.write_text("person@example.com\n", encoding="utf-8")
            self.assertEqual(scan_file(safe_path, "safe.txt"), [])

            lookalike_path = Path(tmp) / "lookalike.txt"
            lookalike_path.write_text("person@notexample.com\n", encoding="utf-8")
            kinds = [k for _, k, _ in scan_file(lookalike_path, "lookalike.txt")]
            self.assertIn("email", kinds)

    def test_env_files_are_scanned_as_text(self):
        self.assertTrue(is_text_file(Path(".env")))
        self.assertTrue(is_text_file(Path(".env.production")))


if __name__ == "__main__":
    unittest.main()
