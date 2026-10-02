import os
from pathlib import Path
import tempfile
import unittest
from review import review_tree


class FileModeTests(unittest.TestCase):
    def test_sensitive_and_world_writable(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "owner.key"
            path.write_text("synthetic", encoding="utf-8")
            path.chmod(0o666)
            self.assertEqual({x["rule"] for x in review_tree(Path(folder))}, {"world-writable", "sensitive-file-exposed"})

    def test_safe_mode_and_symlink(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "owner.key"
            path.write_text("synthetic", encoding="utf-8")
            path.chmod(0o600)
            (Path(folder) / "link.key").symlink_to(path)
            self.assertEqual(review_tree(Path(folder)), [])

    def test_invalid_root(self):
        with self.assertRaises(ValueError):
            review_tree(Path("/definitely/missing/cvp-review"))
