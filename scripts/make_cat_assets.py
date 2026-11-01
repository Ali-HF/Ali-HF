# -*- coding: utf-8 -*-
"""
Generates 100% pixelated Japanese Cyber Cat assets.
Palette (GitHub Dark & Pastel Green):
- Primary Pastel Green (GitHub Primer): #7ee787
- Bright Contribution Green: #39d353
- Light Sage Green: #aff5b4
- Dark Forest Green: #238636
- Deep Green: #0e4429
- GitHub Canvas Dark: #0d1117
- GitHub Surface/Header: #161b22
- GitHub Border: #30363d
- GitHub Muted Text / Steel Grey: #8b949e
- Pure Pitch Black Outline: #010409

Zero smooth gradients. 100% crisp pixelated aesthetic.
"""
import os

CAT_HALF_GRID = [
    "    ##        ", # 0: ear tip
    "   #..#       ", # 1: ear
    "  #....#      ", # 2: ear
    " #......######", # 3: head top
    " #............", # 4: forehead
    " #............", # 5: forehead
    " #...@@@......", # 6: eye top
    "-#..@@@@@.....", # 7: whisker 1 + eye
    " #..@@!@@.....", # 8: eye with shine (!)
    "--#..@@@.....*", # 9: whisker 2 + nose
    " #...........#", # 10: mouth center line
    "-#......#..#..", # 11: mouth w
    "  #......##...", # 12: mouth w bottom
    "   #==========", # 13: collar
    "   #=========o", # 14: collar bell in center
    "   #..........", # 15: paws
    "   #.##..##...", # 16: claws/pads
    "    ##########", # 17: bottom
]

PALETTE = {
    '#': '#010409', # Pitch outline
    '.': '#21262d', # Dark charcoal fur
    '@': '#7ee787', # GitHub pastel green eyes
    '!': '#ffffff', # Eye sparkle
    '*': '#7ee787', # Nose
    '-': '#8b949e', # Whiskers
    '=': '#238636', # Collar
    'o': '#aff5b4', # Collar bell
}

def build_cat_svg(px=4, ox=0, oy=0):
    rects = []
    for y, row in enumerate(CAT_HALF_GRID):
        # Mirror: row[:-1][::-1] mirrors columns 0..12 to the right, keeping col 13 centered
        full_row = row + row[:-1][::-1]
        for x, ch in enumerate(full_row):
            if ch in PALETTE:
                rects.append(f'<rect x="{ox + x * px}" y="{oy + y * px}" width="{px}" height="{px}" fill="{PALETTE[ch]}"/>')
    return "".join(rects)

def generate_avatar():
    size = 200
    # Cat sprite is 27 wide x 18 high
    # With px=6: 27*6 = 162 wide, 18*6 = 108 high
    px = 6
    w_sprite = 27 * px
    h_sprite = 18 * px
    ox = (size - w_sprite) // 2
    oy = (size - h_sprite) // 2 + 10
    
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="{size}" height="{size}" shape-rendering="crispEdges">',
        f'<rect width="{size}" height="{size}" fill="#0d1117"/>',
        # Pixel border (GitHub dark grey & pastel green)
        f'<rect x="2" y="2" width="{size - 4}" height="{size - 4}" fill="none" stroke="#21262d" stroke-width="2"/>',
        f'<rect x="6" y="6" width="{size - 12}" height="{size - 12}" fill="none" stroke="#7ee787" stroke-width="1" stroke-dasharray="8 4"/>',
        # Pixel corner brackets
        '<rect x="10" y="10" width="12" height="2" fill="#7ee787"/>',
        '<rect x="10" y="10" width="2" height="12" fill="#7ee787"/>',
        '<rect x="178" y="10" width="12" height="2" fill="#7ee787"/>',
        '<rect x="188" y="10" width="2" height="12" fill="#7ee787"/>',
        '<rect x="10" y="188" width="12" height="2" fill="#7ee787"/>',
        '<rect x="10" y="178" width="2" height="12" fill="#7ee787"/>',
        '<rect x="178" y="188" width="12" height="2" fill="#7ee787"/>',
        '<rect x="188" y="178" width="2" height="12" fill="#7ee787"/>',
        # HUD text labels
        '<text x="14" y="22" font-family="\'Courier New\', monospace" font-size="9" font-weight="bold" fill="#8b949e">ネコ//01</text>',
        '<text x="142" y="22" font-family="\'Courier New\', monospace" font-size="9" font-weight="bold" fill="#7ee787">PURR_LOCK</text>',
        '<text x="14" y="185" font-family="\'Courier New\', monospace" font-size="9" font-weight="bold" fill="#7ee787">ALI.CAT</text>',
        '<text x="135" y="185" font-family="\'Courier New\', monospace" font-size="9" font-weight="bold" fill="#8b949e">BCIT//NED</text>',
        # The Cat Sprite
        build_cat_svg(px=px, ox=ox, oy=oy),
        '</svg>'
    ]
    return "\n".join(parts)

def generate_header():
    w, h = 820, 160
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}" shape-rendering="crispEdges">',
        f'<rect width="{w}" height="{h}" fill="#0d1117"/>',
        # Outer pixel border
        f'<rect x="2" y="2" width="{w-4}" height="{h-4}" fill="none" stroke="#21262d" stroke-width="2"/>',
        f'<rect x="6" y="6" width="{w-12}" height="{h-12}" fill="none" stroke="#30363d" stroke-width="1"/>',
    ]
    
    # Alternating pixel blocks along top and bottom (pastel green & charcoal, no smooth gradients!)
    for x in range(12, w - 12, 16):
        parts.append(f'<rect x="{x}" y="8" width="8" height="4" fill="#7ee787"/>')
        parts.append(f'<rect x="{x + 8}" y="8" width="8" height="4" fill="#161b22"/>')
        parts.append(f'<rect x="{x}" y="{h-12}" width="8" height="4" fill="#161b22"/>')
        parts.append(f'<rect x="{x + 8}" y="{h-12}" width="8" height="4" fill="#7ee787"/>')
        
    # Left cat (pixel sprite with px=4 -> 27*4 = 108 wide, 18*4 = 72 high)
    parts.append(build_cat_svg(px=4, ox=45, oy=42))
    # Right cat
    parts.append(build_cat_svg(px=4, ox=w - 153, oy=42))
    
    # Center Japanese Typography & HUD
    parts += [
        # Large Katakana 'アリ' (Ali) in crisp pastel green
        '<text x="410" y="70" font-family="\'Press Start 2P\', \'Courier New\', monospace" font-size="44" font-weight="900" fill="#7ee787" text-anchor="middle" letter-spacing="8">アリ</text>',
        # Subtitle
        '<text x="410" y="98" font-family="\'Courier New\', monospace" font-size="13" font-weight="bold" fill="#8b949e" text-anchor="middle" letter-spacing="3">サイバーネコ // CYBER CAT UNIT 01</text>',
        # Telemetry line
        '<text x="410" y="122" font-family="\'Courier New\', monospace" font-size="10" font-weight="bold" fill="#7ee787" text-anchor="middle" letter-spacing="2">[ STATUS: PURRING // SECTOR: KARACHI // OS: BCIT-CAT.SYS ]</text>',
        # Kaomoji top center
        '<text x="410" y="24" font-family="\'Courier New\', monospace" font-size="11" font-weight="bold" fill="#7ee787" text-anchor="middle">(=^･ω･^=)</text>',
        '</svg>'
    ]
    return "\n".join(parts)

def generate_divider():
    w, h = 820, 20
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}" shape-rendering="crispEdges">',
        f'<rect width="{w}" height="{h}" fill="#0d1117"/>',
        # Center rail
        f'<rect x="0" y="9" width="{w}" height="2" fill="#21262d"/>',
        f'<rect x="100" y="8" width="{w - 200}" height="4" fill="#30363d"/>',
    ]
    # Pastel green pixel paw markers
    for x in range(120, w - 120, 44):
        parts.append(f'<rect x="{x}" y="7" width="6" height="6" fill="#7ee787"/>')
    # Center Cat box
    parts += [
        f'<rect x="{w//2 - 45}" y="2" width="90" height="16" fill="#161b22" stroke="#7ee787" stroke-width="1"/>',
        f'<text x="{w//2}" y="14" font-family="\'Courier New\', monospace" font-size="10" font-weight="bold" fill="#7ee787" text-anchor="middle" letter-spacing="1">(=^･ω･^=)</text>',
        '</svg>'
    ]
    return "\n".join(parts)

def generate_beme():
    lines = [
        (">be me", "#7ee787"),
        (">CS student in Karachi", "#8b949e"),
        ('>"just one more commit then sleep"', "#8b949e"),
        (">it is 4am", "#7ee787"),
        (">the bug was a missing semicolon", "#aff5b4"),
        (">mfw (=^･ω･^=)", "#7ee787")
    ]
    width = 780
    height = 230
    line_height = 25
    start_y = 66
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="{height}" shape-rendering="crispEdges">
  <defs>
    <style>
      .terminal-bg {{ fill: #0d1117; stroke: #30363d; stroke-width: 2px; }}
      .header-bar {{ fill: #161b22; }}
      .hud-pip {{ fill: #7ee787; }}
      .hud-pip-dim {{ fill: #30363d; }}
      .window-title {{ font-family: 'Press Start 2P', 'Courier New', monospace; font-size: 10px; fill: #7ee787; letter-spacing: 1px; }}
      .pixel-text {{
        font-family: 'Press Start 2P', 'VT323', 'Courier New', monospace;
        font-size: 11px;
        letter-spacing: 0.5px;
      }}
      .cursor {{
        font-family: 'Press Start 2P', monospace;
        font-size: 11px;
        fill: #7ee787;
        animation: blink 0.8s infinite;
      }}
      @keyframes blink {{
        0%, 49% {{ opacity: 1; }}
        50%, 100% {{ opacity: 0; }}
      }}
      @keyframes lineReveal {{
        0% {{ opacity: 0; transform: translateX(-8px); }}
        100% {{ opacity: 1; transform: translateX(0); }}
      }}
'''
    for i in range(len(lines)):
        delay = 0.2 + i * 0.4
        svg += f'''      .line-{i} {{
        opacity: 0;
        animation: lineReveal 0.4s ease forwards {delay:.2f}s;
      }}
'''
    svg += '''    </style>
  </defs>

  <!-- Frame -->
  <rect x="2" y="2" width="''' + str(width - 4) + '''" height="''' + str(height - 4) + '''" class="terminal-bg"/>
  <rect x="2" y="2" width="''' + str(width - 4) + '''" height="28" class="header-bar"/>
  <rect x="2" y="30" width="''' + str(width - 4) + '''" height="1" fill="#7ee787"/>

  <!-- Pips -->
  <rect x="16" y="10" width="8" height="8" class="hud-pip"/>
  <rect x="28" y="10" width="8" height="8" class="hud-pip-dim"/>
  <rect x="40" y="10" width="8" height="8" class="hud-pip-dim"/>

  <!-- Title -->
  <text x="''' + str(width // 2) + '''" y="19" text-anchor="middle" class="window-title">CAT_LOG // UNIT-01 // >be_me.sh</text>
'''
    for i, (text, col) in enumerate(lines):
        y_pos = start_y + i * line_height
        svg += f'''  <g class="line-{i}">
    <text x="24" y="{y_pos}" fill="{col}" class="pixel-text">{text}</text>
  </g>
'''

    cursor_y = start_y + (len(lines) - 1) * line_height
    svg += f'''  <text x="210" y="{cursor_y}" class="cursor">█</text>
</svg>'''
    return svg

def generate_devnull():
    items = [
        ("head", "Anonymous 10/31/26(Sat)21:20:11 No.31415926", "#8b949e", 24),
        ("body", ">ali pushed to main", "#7ee787", 36),
        ("body", '>commit message: "fix"', "#7ee787", 36),
        ("body", '>commit message: "fix2"', "#7ee787", 36),
        ("body", '>commit message: "fix FINAL"', "#7ee787", 36),
        ("body", '>commit message: "fix FINAL real"', "#7ee787", 36),
        ("space", "", "", 0),
        ("head", "Anonymous 10/31/26(Sat)21:20:48 No.31415927", "#8b949e", 24),
        ("ref", ">>31415926", "#7ee787", 36),
        ("body", "it compiled once on his machine, that's all the QA we need", "#c9d1d9", 36),
        ("space", "", "", 0),
        ("head", "Anonymous 10/31/26(Sat)21:21:30 No.31415928", "#8b949e", 24),
        ("ref", ">>31415927", "#7ee787", 36),
        ("body", "works on my machine is a valid deployment strategy", "#c9d1d9", 36),
    ]

    width = 780
    height = 370
    start_y = 58
    line_height = 20

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="{height}" shape-rendering="crispEdges">
  <defs>
    <style>
      .terminal-bg {{ fill: #0d1117; stroke: #30363d; stroke-width: 2px; }}
      .header-bar {{ fill: #161b22; }}
      .hud-pip {{ fill: #7ee787; }}
      .hud-pip-dim {{ fill: #30363d; }}
      .window-title {{ font-family: 'Press Start 2P', 'Courier New', monospace; font-size: 10px; fill: #7ee787; letter-spacing: 1px; }}
      .pixel-text {{
        font-family: 'Press Start 2P', 'VT323', 'Courier New', monospace;
        font-size: 10px;
        letter-spacing: 0.3px;
      }}
      .cursor {{
        font-family: 'Press Start 2P', monospace;
        font-size: 10px;
        fill: #7ee787;
        animation: blink 0.8s infinite;
      }}
      @keyframes blink {{
        0%, 49% {{ opacity: 1; }}
        50%, 100% {{ opacity: 0; }}
      }}
      @keyframes lineFade {{
        0% {{ opacity: 0; transform: translateY(4px); }}
        100% {{ opacity: 1; transform: translateY(0); }}
      }}
'''
    cur_idx = 0
    for item in items:
        if item[0] != "space":
            delay = 0.2 + cur_idx * 0.22
            svg += f'''      .item-{cur_idx} {{
        opacity: 0;
        animation: lineFade 0.35s ease forwards {delay:.2f}s;
      }}
'''
            cur_idx += 1

    svg += '''    </style>
  </defs>

  <!-- Frame -->
  <rect x="2" y="2" width="''' + str(width - 4) + '''" height="''' + str(height - 4) + '''" class="terminal-bg"/>
  <rect x="2" y="2" width="''' + str(width - 4) + '''" height="28" class="header-bar"/>
  <rect x="2" y="30" width="''' + str(width - 4) + '''" height="1" fill="#7ee787"/>

  <!-- Pips -->
  <rect x="16" y="10" width="8" height="8" class="hud-pip"/>
  <rect x="28" y="10" width="8" height="8" class="hud-pip-dim"/>
  <rect x="40" y="10" width="8" height="8" class="hud-pip-dim"/>

  <!-- Title -->
  <text x="''' + str(width // 2) + '''" y="19" text-anchor="middle" class="window-title">BBS://NEKO-NET/SECTOR-KARACHI/31415926</text>
'''
    y_pos = start_y
    anim_i = 0
    for item in items:
        itype, text, col, x_off = item
        if itype == "space":
            y_pos += 8
            continue
        svg += f'''  <g class="item-{anim_i}">
    <text x="{x_off}" y="{y_pos}" fill="{col}" class="pixel-text">{text}</text>
  </g>
'''
        y_pos += line_height
        anim_i += 1

    svg += f'''  <text x="590" y="{y_pos - line_height}" class="cursor">█</text>
</svg>'''
    return svg

if __name__ == "__main__":
    os.makedirs("assets", exist_ok=True)
    with open("assets/avatar.svg", "w", encoding="utf-8") as f:
        f.write(generate_avatar())
    with open("assets/header.svg", "w", encoding="utf-8") as f:
        f.write(generate_header())
    with open("assets/divider.svg", "w", encoding="utf-8") as f:
        f.write(generate_divider())
    with open("assets/beme.svg", "w", encoding="utf-8") as f:
        f.write(generate_beme())
    with open("assets/devnull.svg", "w", encoding="utf-8") as f:
        f.write(generate_devnull())
    print("Generated all Japanese Cyber Cat pixel assets in pastel GitHub green!")
