"""Generates assets/avatar.svg and assets/divider.svg (pixel art, no dependencies)."""
import os

FONT = {
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    "I": ["11111", "00100", "00100", "00100", "00100", "00100", "11111"],
}

STAR = ["00100", "00100", "11111", "00100", "00100"]
HEART = ["01010", "11111", "11111", "01110", "00100"]


def rects(bitmap, ox, oy, px, color, opacity=1.0):
    out = []
    for y, row in enumerate(bitmap):
        for x, c in enumerate(row):
            if c == "1":
                out.append(
                    f'<rect x="{ox + x * px}" y="{oy + y * px}" width="{px}" height="{px}" '
                    f'fill="{color}" opacity="{opacity}"/>'
                )
    return out


def avatar():
    size = 160
    px = 6
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="{size}" height="{size}" shape-rendering="crispEdges">',
        '<rect width="160" height="160" fill="#0d0221"/>',
        '<rect x="4" y="4" width="152" height="152" fill="none" stroke="#ff2a6d" stroke-width="4"/>',
        '<rect x="12" y="12" width="136" height="136" fill="none" stroke="#05d9e8" stroke-width="2"/>',
    ]
    # letters A L I with a cyan shadow behind a pink face
    x = 22
    for ch in "ALI":
        parts += rects(FONT[ch], x + 3, 52 + 3, px, "#05d9e8")
        parts += rects(FONT[ch], x, 52, px, "#ff2a6d")
        x += 5 * px + 6
    parts += rects(STAR, 18, 18, 4, "#f9c80e")
    parts += rects(HEART, 122, 120, 4, "#ff2a6d")
    # scanlines
    for y in range(0, size, 4):
        parts.append(f'<rect x="0" y="{y}" width="{size}" height="1" fill="#000" opacity="0.18"/>')
    parts.append("</svg>")
    return "\n".join(parts)


def divider():
    w, h, px = 800, 20, 4
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" shape-rendering="crispEdges">',
        f'<rect y="8" width="{w}" height="4" fill="#ff2a6d" opacity="0.35"/>',
    ]
    spots = [(60, STAR, "#05d9e8"), (380, HEART, "#ff2a6d"), (740, STAR, "#f9c80e")]
    for sx, sprite, col in spots:
        parts.append(f'<rect x="{sx - 6}" y="0" width="32" height="{h}" fill="#0d0221"/>')
        parts += rects(sprite, sx, 0, px, col)
    parts.append("</svg>")
    return "\n".join(parts)


if __name__ == "__main__":
    os.makedirs("assets", exist_ok=True)
    open("assets/avatar.svg", "w").write(avatar())
    open("assets/divider.svg", "w").write(divider())
    print("wrote assets/avatar.svg, assets/divider.svg")
