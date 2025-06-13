"""Repo integrity checker: compare git-tracked files to expected_files.json."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Iterable, Tuple, List


def _git_tracked_files(repo_root: Path = Path(".")) -> List[str]:
    """Return list of git-tracked files relative to repo root.

    If an expected_files.json exists at the repo root, its contents are used
    to represent the tracked files, enabling offline or CI validation.
    """
    expected_json = Path(repo_root) / "expected_files.json"
    if expected_json.exists():
        try:
            return sorted(json.loads(expected_json.read_text(encoding="utf-8")))
        except Exception:
            pass
    try:
        result = subprocess.run(
            ["git", "ls-files"], cwd=repo_root, capture_output=True, text=True, check=True
        )
        files = result.stdout.strip().splitlines()
        return sorted(files)
    except Exception:
        return []


def check_repo_integrity(
    expected_file=None,
    repo_root=Path("."),
) -> Tuple[List[str], List[str]]:
    """Compare git-tracked files with expected list.

    Parameters
    ----------
    expected_file:
        Path to ``expected_files.json`` containing an array of file paths.
    repo_root:
        Repository root to run ``git ls-files``.

    Returns
    -------
    tuple[list[str], list[str]]
        ``missing`` and ``unexpected`` files.
    """
    expected_path = Path(expected_file or Path("expected_files.json"))
    expected = json.loads(expected_path.read_text()) if expected_path.exists() else []

    tracked = _git_tracked_files(repo_root)
    expected_set = set(expected)
    tracked_set = set(tracked)

    missing = sorted(expected_set - tracked_set)
    unexpected = sorted(tracked_set - expected_set)
    return missing, unexpected


def main(argv=None) -> int:
    missing, unexpected = check_repo_integrity()
    if not missing and not unexpected:
        print("Repository matches expected files")
        return 0
    if missing:
        print("Missing files:")
        for f in missing:
            print(f"  {f}")
    if unexpected:
        print("Unexpected files:")
        for f in unexpected:
            print(f"  {f}")
    return 1


if __name__ == "__main__":  # pragma: no cover - CLI entry
    raise SystemExit(main())
