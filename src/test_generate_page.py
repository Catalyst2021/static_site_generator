import os
import tempfile
import unittest
from gencontent import generate_page

class TestGeneratePage(unittest.TestCase):
    def test_generate_page(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            md_path = os.path.join(tmpdir, "index.md")
            template_path = os.path.join(tmpdir, "template.html")
            dest_path = os.path.join(tmpdir, "public", "index.html")

            with open(md_path, "w") as f:
                f.write("# Test Page\n\nThis is **bold** text.")

            with open(template_path, "w") as f:
                f.write("<html><head><title>{{ Title }}</title></head><body>{{ Content }}</body></html>")

            generate_page(md_path, template_path, dest_path)

            with open(dest_path, "r") as f:
                html = f.read()

            self.assertIn("<title>Test Page</title>", html)
            self.assertIn("<h1>Test Page</h1>", html)
            self.assertIn("<b>bold</b>", html)

if __name__ == "__main__":
    unittest.main()