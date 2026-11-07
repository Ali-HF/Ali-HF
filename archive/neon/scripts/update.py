"""Daily updater: rotating ASCII banner, neofetch panel, recent pushes, XP bar.
Uses only the standard library, plus pyfiglet if installed (for the banner)."""
import datetime as dt
import json
import math
import os
import re
import urllib.request

USER = os.environ.get("GH_USER", "Ali-HF")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
README = "README.md"


def api(path):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "profile-updater"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    req = urllib.request.Request(f"https://api.github.com{path}", headers=headers)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def replace_block(text, name, content):
    pattern = re.compile(
        rf"(<!--START_SECTION:{name}-->).*?(<!--END_SECTION:{name}-->)", re.DOTALL
    )
    if not pattern.search(text):
        return text
    return pattern.sub(lambda m: f"{m.group(1)}\n{content}\n{m.group(2)}", text)


def code(body):
    return "```text\n" + body.rstrip("\n") + "\n```"


def make_banner(today):
    try:
        import pyfiglet
    except ImportError:
        return None
    fonts = ["ansi_shadow", "slant", "bloody"]
    start = today.timetuple().tm_yday % len(fonts)
    for i in range(len(fonts)):
        try:
            art = pyfiglet.figlet_format("ALI-HF", font=fonts[(start + i) % len(fonts)], width=80)
            return code(art)
        except Exception:
            continue
    return None


def ago(iso):
    t = dt.datetime.strptime(iso, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
    d = dt.datetime.now(dt.timezone.utc) - t
    if d.days >= 1:
        return f"{d.days}d ago"
    if d.seconds >= 3600:
        return f"{d.seconds // 3600}h ago"
    return f"{max(d.seconds // 60, 1)}m ago"


def main():
    today = dt.date.today()
    text = open(README, encoding="utf-8").read()

    banner = make_banner(today)
    if banner:
        text = replace_block(text, "banner", banner)

    try:
        user = api(f"/users/{USER}")
        repos = api(f"/users/{USER}/repos?per_page=100&sort=pushed")
    except Exception as e:  # offline or rate limited: leave live sections untouched
        print("GitHub API unavailable, skipping live sections:", e)
        open(README, "w", encoding="utf-8").write(text)
        return

    repos = [r for r in repos if r["name"] != USER and not r.get("fork")] or repos
    stars = sum(r["stargazers_count"] for r in repos)
    forks = sum(r["forks_count"] for r in repos)
    created = dt.datetime.strptime(user["created_at"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
    days = (dt.datetime.now(dt.timezone.utc) - created).days
    last_push = ago(repos[0]["pushed_at"]) if repos else "n/a"

    neofetch = (
        f"ali@github\n----------\n"
        f"Host      : NED University, Karachi\n"
        f"Class     : BCIT\n"
        f"Guild     : hkh.agency\n"
        f"Side quest: Notebloom\n"
        f"Uptime    : {days} days on GitHub\n"
        f"Repos     : {user['public_repos']}\n"
        f"Stars     : {stars}\n"
        f"Followers : {user['followers']}\n"
        f"Last push : {last_push}\n"
        f"Updated   : {today.isoformat()}"
    )
    text = replace_block(text, "neofetch", code(neofetch))

    lines = [
        "| Repository | Tech Stack | Last Active |",
        "| :--- | :---: | :---: |"
    ]
    for r in repos[:6]:
        lang = f"`{r['language']}`" if r.get("language") else "`Code`"
        lines.append(f"| [**{r['name']}**]({r['html_url']}) | {lang} | {ago(r['pushed_at'])} |")
    text = replace_block(text, "repos", "\n".join(lines) if repos else "_no public repos found_")

    xp = user["public_repos"] * 40 + stars * 25 + forks * 25 + user["followers"] * 30 + days // 10
    level = int(math.sqrt(xp / 20)) + 1
    floor_xp, next_xp = 20 * (level - 1) ** 2, 20 * level ** 2
    frac = (xp - floor_xp) / max(next_xp - floor_xp, 1)
    filled = max(0, min(20, int(frac * 20)))
    ranks = ["NEWBIE", "SCRIPT KIDDIE", "CODE MONKEY", "HACKER", "WIZARD", "LEGEND"]
    rank = ranks[min(level // 3, len(ranks) - 1)]
    bar = "█" * filled + "░" * (20 - filled)
    xp_block = f"LVL {level:02d} [{bar}] {xp} / {next_xp} XP\nCLASS: {rank}"
    text = replace_block(text, "xp", code(xp_block))

    open(README, "w", encoding="utf-8").write(text)
    print("README updated")


if __name__ == "__main__":
    main()
