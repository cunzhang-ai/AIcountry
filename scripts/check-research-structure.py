#!/usr/bin/env python3
"""Check the current research tree without changing historical editions."""

from pathlib import Path
import re
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1] / "research"
CHAPTERS = ROOT / "country"
LINK = re.compile(r"\]\(([^)]+)\)")
SCHEME = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")


def current_files():
    for path in ROOT.rglob("*.md"):
        if not any(part.startswith("2026-") for part in path.relative_to(ROOT).parts):
            yield path


def table_rows(path):
    return [
        line for line in path.read_text().splitlines()
        if line.startswith("| ") and not line.startswith("|---")
    ][1:]


def main():
    failures = []
    files = list(current_files())
    for path in files:
        body = path.read_text()
        if len(body.splitlines()) > 150:
            failures.append(f"{path}: current file exceeds 150 lines")
        for match in LINK.finditer(body):
            raw = match.group(1).strip("<>").split("#", 1)[0].split("?", 1)[0]
            if raw and not SCHEME.match(raw) and not (path.parent / unquote(raw)).exists():
                failures.append(f"{path}: missing local link {raw}")

    for number in range(1, 15):
        prefix = f"C{number:02d}"
        entrances = list(CHAPTERS.glob(f"{prefix}-*.md"))
        if len(entrances) != 1:
            failures.append(f"{prefix}: expected one chapter entrance, found {len(entrances)}")
            continue
        entrance = entrances[0].read_text()
        for topic in (CHAPTERS / prefix).glob("*.md"):
            if f"{prefix}/{topic.name}" not in entrance:
                failures.append(f"{entrances[0]}: topic absent from chapter map: {topic.name}")

    audit_files = sorted((ROOT / "coverage").glob("*.md"))
    if len(audit_files) != 4:
        failures.append(f"coverage: expected four system files, found {len(audit_files)}")
    findings = []
    for path in audit_files:
        findings.extend(row.split(" | ", 1)[0][2:] for row in table_rows(path))
    if len(findings) != len(set(findings)):
        failures.append("coverage: a state function has more than one owner")
    if not findings:
        failures.append("coverage: no functional findings")

    if failures:
        print("Research organization check failed:")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)
    print(f"Research organization OK: {len(files)} current files, 14 chapters, "
          f"{len(findings)} single-owned audit findings, local links resolved.")


if __name__ == "__main__":
    main()
