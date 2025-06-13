from pathlib import Path

from repo_integrity_checker import check_repo_integrity


def test_repo_matches_expected(tmp_path, monkeypatch):
    expected_path = Path('expected_files.json')
    if not expected_path.exists():
        raise RuntimeError('expected_files.json missing')

    missing, unexpected = check_repo_integrity(expected_path)
    assert missing == []
    assert unexpected == []
