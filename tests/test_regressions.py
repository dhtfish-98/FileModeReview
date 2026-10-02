import json
import plistlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from review import review_tree


class RegressionTests(unittest.TestCase):

    def test_env_variant_is_reviewed(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            path=root/".env.production"
            path.write_text("synthetic")
            path.chmod(0o644)
            self.assertEqual([x["rule"] for x in review_tree(root)],["sensitive-file-exposed"])
