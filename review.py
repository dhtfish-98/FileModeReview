"""Inspect local file modes without following links or reading file contents."""

from __future__ import annotations

import os
from pathlib import Path
import stat

SENSITIVE_SUFFIXES = (".pem", ".key", ".p12", ".env")


def review_tree(root: Path) -> list[dict[str, str]]:
    root = Path(root)
    if root.is_symlink() or not root.is_dir():
        raise ValueError("root must be a real directory")
    findings = []
    def fail(error: OSError) -> None:
        raise error

    for current, directories, files in os.walk(root, followlinks=False, onerror=fail):
        directories[:] = sorted(name for name in directories if not (Path(current) / name).is_symlink())
        for name in sorted(files):
            path = Path(current) / name
            mode = path.lstat().st_mode
            if not stat.S_ISREG(mode):
                continue
            rel = path.relative_to(root).as_posix()
            if mode & stat.S_IWOTH:
                findings.append({"rule": "world-writable", "location": rel, "note": "World-write mode bit is set; review effective access"})
            if (path.name.lower().endswith(SENSITIVE_SUFFIXES) or path.name.lower().startswith(".env.")) and mode & (stat.S_IRWXG | stat.S_IRWXO):
                findings.append({"rule": "sensitive-file-exposed", "location": rel, "note": "Sensitive-name file has group or other permissions"})
    return findings
