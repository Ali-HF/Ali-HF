"""Handles guestbook + tic-tac-toe issues, and re-renders both README sections.
Env: ISSUE_TITLE, ISSUE_BODY, ISSUE_AUTHOR.  `python scripts/interact.py render` just re-renders."""
import datetime as dt
import json
import os
import random
import re
import sys

USER = os.environ.get("GH_USER", "Ali-HF")
REPO = f"{USER}/{USER}"
README = "README.md"
GB = "data/guestbook.json"
TT = "data/ttt.json"
LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]


def load(path, default):
    try:
        return json.load(open(path, encoding="utf-8"))
    except Exception:
        return default


def save(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(obj, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)


def replace_block(text, name, content):
    pattern = re.compile(
        rf"(<!--START_SECTION:{name}-->).*?(<!--END_SECTION:{name}-->)", re.DOTALL
    )
    return pattern.sub(lambda m: f"{m.group(1)}\n{content}\n{m.group(2)}", text)


# ---------- tic-tac-toe ----------
def new_state(wins=None):
    return {"board": [""] * 9, "status": "playing", "wins": wins or {"x": 0, "o": 0, "draw": 0}, "last": ""}


def winner(b):
    for a, c, d in LINES:
        if b[a] and b[a] == b[c] == b[d]:
            return b[a]
    return None


def bot_move(b):
    empties = [i for i, v in enumerate(b) if not v]
    for mark in ("O", "X"):  # win first, then block
        for line in LINES:
            vals = [b[i] for i in line]
            if vals.count(mark) == 2 and vals.count("") == 1:
                return line[vals.index("")]
    if 4 in empties:
        return 4
    corners = [i for i in (0, 2, 6, 8) if i in empties]
    return random.choice(corners or empties)


def finish(s):
    w = winner(s["board"])
    if w:
        s["status"] = w.lower()
        s["wins"][w.lower()] += 1
    elif all(s["board"]):
        s["status"] = "draw"
        s["wins"]["draw"] += 1


def handle_ttt(title, author):
    s = load(TT, None) or new_state()
    parts = title.split("|")
    cmd = parts[1] if len(parts) > 1 else ""
    if cmd == "new":
        save(TT, new_state(s["wins"]))
        return
    if cmd != "move" or len(parts) < 3 or not parts[2].strip().isdigit():
        return
    idx = int(parts[2])
    if not 0 <= idx <= 8:
        return
    if s["status"] != "playing":
        s = new_state(s["wins"])
    if s["board"][idx]:
        return
    s["board"][idx] = "X"
    s["last"] = re.sub(r"[^A-Za-z0-9-]", "", author)[:39]
    finish(s)
    if s["status"] == "playing":
        s["board"][bot_move(s["board"])] = "O"
        finish(s)
    save(TT, s)


def render_ttt():
    s = load(TT, None) or new_state()
    sym = {"X": "🐾", "O": "⚫"}
    base = f"https://github.com/{REPO}/issues/new?labels=ttt&body=Just+press+Submit+new+issue.+The+bot+does+the+rest.&title="
    rows = ["| &nbsp; | &nbsp; | &nbsp; |", "|:-:|:-:|:-:|"]
    for r in range(3):
        cells = []
        for c in range(3):
            i = r * 3 + c
            v = s["board"][i]
            if v:
                cells.append(sym[v])
            elif s["status"] == "playing":
                cells.append(f"[🔲]({base}ttt%7Cmove%7C{i})")
            else:
                cells.append("⬛")
        rows.append("| " + " | ".join(cells) + " |")
    msg = {
        "playing": "your move (you are 🐾)",
        "x": "🐾 wins! (=^･ω･^=) click any square for a new game",
        "o": "⚫ the bot wins. click any square for a rematch",
        "draw": "draw. click any square to go again",
    }[s["status"]]
    w = s["wins"]
    last = f" last move by @{s['last']}" if s["last"] else ""
    foot = f"**{msg}**{last}<br>score: you 🐾 {w['x']} | bot ⚫ {w['o']} | draws {w['draw']} · [reset board]({base}ttt%7Cnew%7C0)"
    return "\n".join(rows) + "\n\n" + foot


# ---------- guestbook ----------
def clean_msg(body):
    for line in (body or "").splitlines():
        line = line.strip()
        if line:
            break
    else:
        return ""
    line = re.sub(r"https?://\S+|www\.\S+", "[link removed]", line)
    line = re.sub(r"[<>|`\[\]\\]", "", line)
    line = re.sub(r"\s+", " ", line).strip()
    if line.lower().startswith("write your message here"):
        return ""
    return line[:140]


def handle_guestbook(body, author):
    msg = clean_msg(body)
    if not msg:
        return
    user = re.sub(r"[^A-Za-z0-9-]", "", author)[:39] or "anon"
    entries = load(GB, [])
    entries.append({"user": user, "msg": msg, "date": dt.date.today().isoformat()})
    save(GB, entries[-50:])


def render_gb():
    entries = load(GB, [])
    if not entries:
        return "```text\nThe wall is empty. Be the first anon.\n```"
    lines = ["+--[ THE WALL ]------------------------------"]
    for e in reversed(entries[-12:]):
        lines.append(f"| [{e['date']}] {e['user']}: {e['msg']}")
    lines.append("+---------------------------------------------")
    return "```text\n" + "\n".join(lines) + "\n```"


def main():
    title = os.environ.get("ISSUE_TITLE", "").strip()
    body = os.environ.get("ISSUE_BODY", "")
    author = os.environ.get("ISSUE_AUTHOR", "anon")
    if len(sys.argv) < 2 or sys.argv[1] != "render":
        if title.lower().startswith("ttt|"):
            handle_ttt(title, author)
        elif title.lower().startswith("guestbook"):
            handle_guestbook(body, author)
    text = open(README, encoding="utf-8").read()
    text = replace_block(text, "ttt", render_ttt())
    text = replace_block(text, "guestbook", render_gb())
    open(README, "w", encoding="utf-8").write(text)
    print("rendered")


if __name__ == "__main__":
    main()
