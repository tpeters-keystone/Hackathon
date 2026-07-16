#!/usr/bin/env python3
"""Update a user's heartbeat and summarize every progress file in the repository."""

from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path

START = "<!-- heartbeat-managed:start -->"
END = "<!-- heartbeat-managed:end -->"
SECTION_NAMES = (
    "Current Focus",
    "Status",
    "Blockers",
    "Needs From Others",
    "Next Steps",
)


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def extract_section(text: str, heading: str) -> str:
    pattern = re.compile(
        rf"^##\s+{re.escape(heading)}\s*$\n(.*?)(?=^##\s+|^<!-- heartbeat-managed:start -->|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    if not match:
        return "Not provided."
    value = re.sub(r"\s+", " ", match.group(1).strip())
    return value or "Not provided."


def first_sentence(value: str, limit: int = 240) -> str:
    value = value.strip()
    if len(value) <= limit:
        return value
    return value[: limit - 1].rstrip() + "…"


def replace_managed_block(text: str, block: str) -> str:
    managed = f"{START}\n{block.rstrip()}\n{END}"
    if START in text and END in text:
        pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.DOTALL)
        return pattern.sub(managed, text, count=1)
    return text.rstrip() + "\n\n" + managed + "\n"


def create_progress_file(path: Path, username: str) -> None:
    path.write_text(
        f"""# {username} Progress

## Current Focus

Not yet provided.

## Status

Progress file created by the repository heartbeat.

## Blockers

None reported.

## Needs From Others

None reported.

## Next Steps

Update this file with the current work plan.
""",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", required=True, help="Username whose heartbeat block should be updated")
    parser.add_argument("--repo", default=None, help="Repository root; defaults to the script's parent repository")
    args = parser.parse_args()

    repo = Path(args.repo).resolve() if args.repo else Path(__file__).resolve().parents[1]
    username = re.sub(r"[^A-Za-z0-9_.-]", "-", args.username).strip("-.")
    if not username:
        raise SystemExit("Username contains no safe filename characters")

    progress_files = sorted(repo.glob("*_progress.md"), key=lambda path: path.name.lower())
    owner_file = repo / f"{username}_progress.md"
    if not owner_file.exists():
        create_progress_file(owner_file, username)
        progress_files = sorted(repo.glob("*_progress.md"), key=lambda path: path.name.lower())

    timestamp = utc_now()
    others = [path for path in progress_files if path.resolve() != owner_file.resolve()]
    heartbeat = f"""## Repository Heartbeat

- Last heartbeat: {timestamp}
- Progress files observed: {len(progress_files)}
- Other contributors checked: {len(others)}
- Coordination digest: [`coordination/status.md`](coordination/status.md)
"""
    owner_text = owner_file.read_text(encoding="utf-8")
    owner_file.write_text(replace_managed_block(owner_text, heartbeat), encoding="utf-8")

    rows = []
    details = []
    for path in progress_files:
        text = path.read_text(encoding="utf-8")
        contributor = path.name[: -len("_progress.md")]
        focus = first_sentence(extract_section(text, "Current Focus"))
        status = first_sentence(extract_section(text, "Status"))
        blockers = first_sentence(extract_section(text, "Blockers"))
        needs = first_sentence(extract_section(text, "Needs From Others"))
        rows.append(f"| `{contributor}` | {focus.replace('|', '\\|')} | {blockers.replace('|', '\\|')} | {needs.replace('|', '\\|')} |")
        details.append(
            f"""## {contributor}

**Source:** [`{path.name}`](../{path.name})

**Current focus:** {focus}

**Status:** {status}

**Blockers:** {blockers}

**Needs from others:** {needs}
"""
        )

    digest = f"""# Coordination Status

> Generated automatically from every root-level `*_progress.md` file. Contributors should edit their own progress file, not this digest.

**Last generated:** {timestamp}

**Progress files checked:** {len(progress_files)}

| Contributor | Current focus | Blockers | Needs from others |
|---|---|---|---|
{chr(10).join(rows)}

# Contributor Details

{chr(10).join(details)}
"""
    coordination = repo / "coordination"
    coordination.mkdir(parents=True, exist_ok=True)
    (coordination / "status.md").write_text(digest, encoding="utf-8")
    print(f"Updated {owner_file.name}; checked {len(progress_files)} progress file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
