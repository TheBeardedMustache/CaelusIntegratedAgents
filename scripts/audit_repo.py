"""CLI entry point for repository audits."""
from __future__ import annotations
from typing import Optional, List

import argparse
from pathlib import Path
import sys

from termcolor import cprint

# Allow running this script directly without installing the project
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from repo_integrity_checker import check_repo_integrity


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Audit repository contents")
    parser.add_argument(
        "--expected-file",
        type=Path,
        default="expected_files.json",
        help="JSON file with the list of expected repo files",
    )
    args = parser.parse_args(argv)

    missing, unexpected = check_repo_integrity(args.expected_file)

    if not missing and not unexpected:
        cprint("Repository matches expected files", "green")
        return 0

    if missing:
        cprint("Missing files:", "red")
        for f in missing:
            print(f"  {f}")
    if unexpected:
        cprint("Unexpected files:", "yellow")
        for f in unexpected:
            print(f"  {f}")
    return 1


if __name__ == "__main__":  # pragma: no cover - script entry
    raise SystemExit(main())
