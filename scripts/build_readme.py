#!/usr/bin/env python3
"""
scripts/build_readme.py
Rebuilds dynamic sections of README.md using HTML comment markers.
Standard library only + pyfiglet.
"""

from datetime import datetime, timezone
import json
import os
import pathlib
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

try:
    import pyfiglet
except ImportError:
    print("Error: pyfiglet is required. Run 'pip install pyfiglet'.", file=sys.stderr)
    sys.exit(1)

FONTS = [
    "standard",
    "slant",
    "big",
    "doom",
    "small",
    "ogre",
    "rectangles",
    "smslant",
    "shadow",
]

ROOT = pathlib.Path(__file__).resolve().parent.parent
README_PATH = ROOT / "README.md"


def replace_chunk(content: str, marker: str, chunk: str, inline: bool = False) -> str:
    """Replaces content between <!-- marker starts --> and <!-- marker ends -->."""
    pattern = re.compile(
        rf"<!-- {marker} starts -->.*<!-- {marker} ends -->",
        re.DOTALL,
    )
    if not inline:
        chunk = f"\n{chunk.strip()}\n"
    replacement = f"<!-- {marker} starts -->{chunk}<!-- {marker} ends -->"
    return pattern.sub(replacement, content)


def generate_banner() -> str:
    """Generates the dripping AliHF banner using pyfiglet 'bloody' font."""
    raw = pyfiglet.figlet_format("AliHF", font="bloody")
    lines = [line.rstrip() for line in raw.splitlines()]

    # Strip leading and trailing empty lines
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()

    banner_text = "\n".join(lines)
    return f"```text\n{banner_text}\n```"


def format_relative_time(dt_str: str) -> str:
    """Formats an ISO-8601 timestamp into human-readable relative time."""
    try:
        dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
    except ValueError:
        return dt_str

    now = datetime.now(timezone.utc)
    diff = now - dt
    seconds = int(diff.total_seconds())

    if seconds < 0:
        return "just now"
    minutes = seconds // 60
    hours = minutes // 60
    days = diff.days

    if days > 365:
        years = days // 365
        return f"{years} year{'s' if years != 1 else ''} ago"
    if days > 30:
        months = days // 30
        return f"{months} month{'s' if months != 1 else ''} ago"
    if days > 1:
        return f"{days} days ago"
    if days == 1:
        return "yesterday"
    if hours >= 1:
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    if minutes >= 1:
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    return "just now"


def fetch_recent_pushes(username: str = "Ali-HF") -> list[str] | None:
    """
    Fetches the 5 most recently pushed non-fork public repos (excluding profile repo)
    from the GitHub REST API.
    Returns None if the API call fails so caller leaves content untouched.
    """
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    url = f"https://api.github.com/users/{username}/repos?sort=pushed&per_page=30"

    headers = {
        "User-Agent": "build-readme-script",
        "Accept": "application/vnd.github.v3+json",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as exc:
        print(f"Warning: Failed to fetch repos from GitHub API: {exc}", file=sys.stderr)
        return None

    if not isinstance(data, list):
        print("Warning: GitHub API returned unexpected response format.", file=sys.stderr)
        return None

    non_forks = []
    for repo in data:
        name = repo.get("name", "")
        # Filter out forks, profile repo, and private repos
        if repo.get("fork"):
            continue
        if name.lower() == username.lower():
            continue
        if repo.get("private"):
            continue
        non_forks.append(repo)

    # Sort descending by pushed_at just in case
    non_forks.sort(key=lambda r: r.get("pushed_at") or "", reverse=True)
    top_repos = non_forks[:5]

    lines = []
    for r in top_repos:
        name = r.get("name")
        html_url = r.get("html_url")
        pushed_at = r.get("pushed_at") or ""
        time_ago = format_relative_time(pushed_at) if pushed_at else ""

        if time_ago:
            lines.append(f"[{name}]({html_url}) - {time_ago}")
        else:
            lines.append(f"[{name}]({html_url})")

    return lines


def fetch_tils(til_dir: pathlib.Path) -> list[str]:
    """
    Finds the 5 newest files in til/ (named YYYY-MM-DD-title.md),
    reads the first '# ' heading as title, and links to the file.
    """
    if not til_dir.exists():
        return []

    files = [f for f in til_dir.glob("*.md") if f.is_file()]
    # Sort files by name in reverse chronological order
    files.sort(key=lambda f: f.name, reverse=True)

    items = []
    for path in files[:5]:
        title = None
        try:
            with path.open("r", encoding="utf-8") as f:
                for line in f:
                    stripped = line.strip()
                    if stripped.startswith("# "):
                        title = stripped[2:].strip()
                        break
        except Exception as exc:
            print(f"Warning: could not read {path}: {exc}", file=sys.stderr)

        if not title:
            # Fallback to filename without date and extension
            parts = path.stem.split("-", 3)
            title = parts[-1].replace("-", " ").capitalize() if len(parts) > 3 else path.stem

        rel_path = f"til/{path.name}"
        # Extract date from filename if available (YYYY-MM-DD)
        date_match = re.match(r"^(\d{4}-\d{2}-\d{2})", path.name)
        if date_match:
            date_str = date_match.group(1)
            items.append(f"[{title}]({rel_path}) - {date_str}")
        else:
            items.append(f"[{title}]({rel_path})")

    return items


def fetch_blog_feed(feed_url: str) -> list[str] | None:
    """Optional helper to fetch items from an RSS or Atom feed."""
    req = urllib.request.Request(feed_url, headers={"User-Agent": "build-readme-script"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read()
        root = ET.fromstring(content)
    except Exception as exc:
        print(f"Warning: Failed to fetch BLOG_FEED: {exc}", file=sys.stderr)
        return None

    entries = []
    # Atom entries
    atom_entries = root.findall(".//{http://www.w3.org/2005/Atom}entry") or root.findall(".//entry")
    if atom_entries:
        for entry in atom_entries[:5]:
            title_el = entry.find("{http://www.w3.org/2005/Atom}title") or entry.find("title")
            title = title_el.text.strip() if title_el is not None and title_el.text else "Untitled"
            link_el = entry.find("{http://www.w3.org/2005/Atom}link") or entry.find("link")
            link = ""
            if link_el is not None:
                link = link_el.get("href") or (link_el.text.strip() if link_el.text else "")
            pub_el = (
                entry.find("{http://www.w3.org/2005/Atom}published")
                or entry.find("{http://www.w3.org/2005/Atom}updated")
                or entry.find("published")
                or entry.find("updated")
            )
            date_str = pub_el.text.strip()[:10] if pub_el is not None and pub_el.text else ""
            if link:
                suffix = f" - {date_str}" if date_str else ""
                entries.append(f"[{title}]({link}){suffix}")
        return entries

    # RSS items
    rss_items = root.findall(".//item")
    if rss_items:
        for item in rss_items[:5]:
            title_el = item.find("title")
            title = title_el.text.strip() if title_el is not None and title_el.text else "Untitled"
            link_el = item.find("link")
            link = link_el.text.strip() if link_el is not None and link_el.text else ""
            pub_el = item.find("pubDate")
            date_str = pub_el.text.strip()[:16] if pub_el is not None and pub_el.text else ""
            if link:
                suffix = f" - {date_str}" if date_str else ""
                entries.append(f"[{title}]({link}){suffix}")
        return entries

    return entries


def main():
    if not README_PATH.exists():
        print(f"Error: {README_PATH} does not exist.", file=sys.stderr)
        sys.exit(1)

    content = README_PATH.read_text(encoding="utf-8")
    updated = content

    # 1. Banner
    if "<!-- banner starts -->" in content:
        banner_chunk = generate_banner()
        updated = replace_chunk(updated, "banner", banner_chunk)
        print("Updated banner.")

    # 2. Recent Pushes
    if "<!-- recent_pushes starts -->" in content:
        pushes = fetch_recent_pushes()
        if pushes is not None:
            if pushes:
                chunk = "\n\n".join(pushes)
            else:
                chunk = "*No recent public pushes.*"
            updated = replace_chunk(updated, "recent_pushes", chunk)
            print(f"Updated recent_pushes ({len(pushes)} entries).")
        else:
            print("Skipped updating recent_pushes due to API error (content untouched).")

    # 3. TILs
    if "<!-- tils starts -->" in content:
        tils = fetch_tils(ROOT / "til")
        if tils:
            chunk = "\n\n".join(tils)
        else:
            chunk = "*No TILs yet.*"
        updated = replace_chunk(updated, "tils", chunk)
        print(f"Updated tils ({len(tils)} entries).")

    # 4. Optional Writing / Blog Feed
    blog_feed = os.environ.get("BLOG_FEED")
    if blog_feed and "<!-- writing starts -->" in content:
        feed_entries = fetch_blog_feed(blog_feed)
        if feed_entries is not None:
            if feed_entries:
                chunk = "\n\n".join(feed_entries)
            else:
                chunk = "*No posts found.*"
            updated = replace_chunk(updated, "writing", chunk)
            print(f"Updated writing from {blog_feed} ({len(feed_entries)} entries).")

    if updated != content:
        README_PATH.write_text(updated, encoding="utf-8")
        print("Successfully updated README.md.")
    else:
        print("README.md is already up to date.")


if __name__ == "__main__":
    main()

