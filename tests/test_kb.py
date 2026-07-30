import json
import tempfile
import unittest
from pathlib import Path

from scripts.check_sensitive_data import scan_file
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

    def test_slugify(self):
        self.assertEqual(slugify("Hello World"), "hello-world")


class NewArticleIdTest(unittest.TestCase):
    def test_next_id_increments(self):
        # Uses repository content; sample article KB-2026-0001 exists.
        nxt = next_article_id("2026")
        self.assertTrue(ARTICLE_ID_RE.match(nxt))
        self.assertGreaterEqual(int(nxt.split("-")[2]), 2)


class SensitiveScanTest(unittest.TestCase):
    def test_detects_private_key(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "leak.txt"
            path.write_text("-----BEGIN " + "PRIVATE KEY-----\nABC\n", encoding="utf-8")
            findings = scan_file(path, "leak.txt")
            kinds = [k for _, k, _ in findings]
            self.assertIn("private_key", kinds)

    def test_allows_redacted(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ok.txt"
            path.write_text("token=[REDACTED_API_KEY]\n", encoding="utf-8")
            findings = scan_file(path, "ok.txt")
            self.assertEqual(findings, [])


if __name__ == "__main__":
    unittest.main()
