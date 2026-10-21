#!/usr/bin/env python3
"""Validate the repository's agent-context and OKF continuity structure."""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "llm-wiki"
OLD_OKF_URL = (
    "https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md"
)
PAGE = ROOT / "zipper-merge-lab.html"
VENDOR_FILES = {"CLAUDE.md", "CLAUDE.local.md", "GEMINI.md"}
LOCAL_PATH_RE = re.compile(r"/Users/[A-Za-z0-9._-]+/|/home/[A-Za-z0-9._-]+/")
VALID_STATUSES = {"draft", "stable", "deprecated"}
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
TOP_LEVEL_KEY_RE = re.compile(r"^([A-Za-z0-9_-]+):(?:\s*(.*))?$")
FENCE_RE = re.compile(r"^(```|~~~).*?^\1", re.MULTILINE | re.DOTALL)
LOG_DATE_RE = re.compile(r"^## (\d{4}-\d{2}-\d{2})$", re.MULTILINE)

errors: list[str] = []
warnings: list[str] = []


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def frontmatter(path: Path) -> tuple[dict[str, str], list[str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        errors.append(f"{relative(path)}: concept is missing opening YAML frontmatter")
        return {}, []
    try:
        closing = lines.index("---", 1)
    except ValueError:
        errors.append(f"{relative(path)}: concept is missing closing YAML frontmatter")
        return {}, []

    raw = lines[1:closing]
    data: dict[str, str] = {}
    for line_number, line in enumerate(raw, start=2):
        if "\t" in line:
            errors.append(f"{relative(path)}:{line_number}: tab in YAML frontmatter")
        if not line or line.isspace() or line.lstrip().startswith(("#", "-")):
            continue
        if line.startswith(" "):
            if not re.match(r"^\s+[A-Za-z0-9_-]+:", line):
                errors.append(
                    f"{relative(path)}:{line_number}: malformed nested YAML entry"
                )
            continue
        match = TOP_LEVEL_KEY_RE.match(line)
        if not match:
            errors.append(f"{relative(path)}:{line_number}: malformed YAML entry")
            continue
        data[match.group(1)] = (match.group(2) or "").strip().strip("'\"")
    return data, raw


def local_target(source: Path, raw_target: str) -> Path | None:
    target = raw_target.strip().strip("<>")
    if target.startswith(("http://", "https://", "mailto:", "tel:", "#")):
        return None
    target = unquote(target.split("#", 1)[0])
    if not target:
        return None
    return (source.parent / target).resolve()


def validate_links(path: Path) -> None:
    # Links inside fenced code blocks are template examples, not live links.
    text = FENCE_RE.sub("", path.read_text(encoding="utf-8"))
    for raw_target in LINK_RE.findall(text):
        target = local_target(path, raw_target)
        if target is not None and not target.exists():
            errors.append(f"{relative(path)}: unresolved relative link {raw_target!r}")


def validate_source_paths(path: Path, raw_frontmatter: list[str]) -> None:
    for line in raw_frontmatter:
        match = re.match(r"^\s+resource:\s*(.+?)\s*$", line)
        if not match:
            continue
        raw_target = match.group(1).strip().strip("'\"")
        target = local_target(path, raw_target)
        if target is not None and raw_target.startswith((".", "/")) and not target.exists():
            errors.append(
                f"{relative(path)}: unresolved frontmatter resource {raw_target!r}"
            )


def nested_events(raw_frontmatter: list[str], key: str) -> list[dict[str, str]]:
    """Read the small mapping/list subset used by OKF lifecycle metadata."""
    events: list[dict[str, str]] = []
    in_block = False
    current: dict[str, str] | None = None
    for line in raw_frontmatter:
        if not in_block:
            if line == f"{key}:":
                in_block = True
            continue
        if line and not line.startswith(" "):
            break
        match = re.match(r"^\s+(-\s+)?([A-Za-z0-9_-]+):\s*(.*?)\s*$", line)
        if not match:
            continue
        starts_event, item_key, value = match.groups()
        if starts_event or current is None:
            current = {}
            events.append(current)
        current[item_key] = value.strip().strip("'\"")
    return events


def validate_lifecycle(path: Path, data: dict[str, str], raw: list[str]) -> None:
    for key in ("generated", "modified", "verified"):
        if key not in data:
            continue
        events = nested_events(raw, key)
        if not events and data[key] != "[]":
            errors.append(f"{relative(path)}: malformed {key} lifecycle metadata")
            continue
        for index, event in enumerate(events):
            actor = event.get("by", "").strip()
            stamp = event.get("at", "").strip()
            label = f"{relative(path)}: {key}[{index}]"
            if not actor:
                errors.append(f"{label} has no actor")
            try:
                parsed = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
                if parsed.tzinfo is None:
                    raise ValueError
            except ValueError:
                errors.append(f"{label} timestamp needs an explicit UTC offset")


def validate_page() -> None:
    """The page must exist, keep its title, and its inline simulation script must parse."""
    if not PAGE.exists():
        errors.append("zipper-merge-lab.html: missing simulation page")
        return
    html = PAGE.read_text(encoding="utf-8")
    if "<title>Zipper Merge Lab</title>" not in html[:8192]:
        errors.append("zipper-merge-lab.html: <title> missing or changed")
    scripts = re.findall(r"<script>(.*?)</script>", html, re.S)
    if not scripts:
        errors.append("zipper-merge-lab.html: no inline simulation script found")
        return
    node = shutil.which("node")
    if node is None:
        warnings.append("node not found; skipped page script syntax check")
        return
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as handle:
        handle.write(scripts[-1])
    result = subprocess.run([node, "--check", handle.name], capture_output=True, text=True)
    Path(handle.name).unlink()
    if result.returncode != 0:
        lines = result.stderr.strip().splitlines()
        detail = next((line for line in lines if "Error" in line), lines[0] if lines else "unknown error")
        errors.append(f"zipper-merge-lab.html: page script does not parse ({detail})")


def main() -> int:
    agents = ROOT / "AGENTS.md"
    if not agents.exists():
        errors.append("AGENTS.md: missing root agent instructions")
    else:
        agents_text = agents.read_text(encoding="utf-8")
        line_count = len(agents_text.splitlines())
        if line_count > 200:
            errors.append(f"AGENTS.md: {line_count} lines exceeds the 200-line ceiling")
        elif line_count > 150:
            warnings.append(
                f"AGENTS.md: {line_count} lines is in the 150-200 review range"
            )
        if len(agents_text.encode("utf-8")) > 12_000:
            warnings.append("AGENTS.md exceeds the 12 KB density warning")

    for path in ROOT.rglob("*"):
        if path.name in VENDOR_FILES and ".git" not in path.parts:
            errors.append(f"{relative(path)}: obsolete vendor-specific instructions are present")

    active_docs = [
        agents,
        ROOT / "README.md",
        *sorted((ROOT / "docs").rglob("*.md")),
        *sorted(WIKI.rglob("*.md")),
    ]
    for path in active_docs:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        if OLD_OKF_URL in text:
            errors.append(f"{relative(path)}: obsolete active OKF specification URL")
        validate_links(path)
        if LOCAL_PATH_RE.search(text):
            errors.append(f"{relative(path)}: contains a local absolute path")

    root_index = WIKI / "index.md"
    if not root_index.exists():
        errors.append("llm-wiki/index.md: missing OKF root index")
    else:
        index_data, _ = frontmatter(root_index)
        if index_data.get("okf_version") != "0.2":
            errors.append('llm-wiki/index.md: expected okf_version: "0.2"')
        extra = set(index_data) - {"okf_version"}
        if extra:
            errors.append(
                f"llm-wiki/index.md: unsupported index metadata {sorted(extra)}"
            )

    log = WIKI / "log.md"
    if not log.exists():
        errors.append("llm-wiki/log.md: missing maintenance log")
    else:
        log_text = log.read_text(encoding="utf-8")
        if log_text.startswith("---"):
            errors.append("llm-wiki/log.md: reserved log must not use concept frontmatter")
        dates = LOG_DATE_RE.findall(log_text)
        if dates != sorted(dates, reverse=True):
            errors.append("llm-wiki/log.md: dated entries must be newest first")

    for path in sorted(WIKI.rglob("*.md")):
        if path.name in {"index.md", "log.md"}:
            continue
        data, raw = frontmatter(path)
        if not data.get("type"):
            errors.append(f"{relative(path)}: concept has no non-empty type")
        status = data.get("status")
        if status and status not in VALID_STATUSES:
            errors.append(
                f"{relative(path)}: invalid status {status!r}; "
                f"expected one of {sorted(VALID_STATUSES)}"
            )
        validate_source_paths(path, raw)
        validate_lifecycle(path, data, raw)

    validate_page()

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        print(
            f"Repository context check failed with {len(errors)} error(s) "
            f"and {len(warnings)} warning(s)."
        )
        return 1

    print(f"Repository context check passed with {len(warnings)} warning(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
