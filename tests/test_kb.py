import tempfile
import unittest
from pathlib import Path

from scripts.build_site import reset_articles_output
from scripts.check_sensitive_data import is_text_file, scan_file
from scripts.kb import ARTICLE_ID_RE, html_escape, markdown_to_html
from scripts.new_article import next_article_id, slugify


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
    def test_next_id_increments(self):
        # Uses repository content; sample article KB-2026-0001 exists.
        nxt = next_article_id("2026")
        self.assertTrue(ARTICLE_ID_RE.match(nxt))
        self.assertGreaterEqual(int(nxt.split("-")[2]), 2)


class GeneratedOutputTest(unittest.TestCase):
    def test_reset_articles_output_removes_stale_pages(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "articles"
            stale = output / "2026" / "kb-2026-9999-stale" / "index.html"
            stale.parent.mkdir(parents=True)
            stale.write_text("stale", encoding="utf-8")

            reset_articles_output(output)

            self.assertTrue(output.is_dir())
            self.assertEqual(list(output.iterdir()), [])


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
