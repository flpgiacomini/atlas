from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parents[3]
OUTPUT = WORKSPACE / "manifests" / "A9_7_RELEASE_SHA256.csv"


def tracked_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=WORKSPACE,
        check=True,
        capture_output=True,
    )
    return sorted(
        path.decode("utf-8")
        for path in result.stdout.split(b"\0")
        if path and path.decode("utf-8") != "manifests/A9_7_RELEASE_SHA256.csv"
    )


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    rows = []
    for relative in tracked_files():
        absolute = WORKSPACE / relative
        rows.append((relative, absolute.stat().st_size, sha256(absolute)))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(("path", "bytes", "sha256"))
        writer.writerows(rows)
    print({"passed": True, "files": len(rows), "output": str(OUTPUT.relative_to(WORKSPACE))})


if __name__ == "__main__":
    main()
