# -*- coding: utf-8 -*-
"""
Generates 100% pixelated Japanese Cyber Mecha assets.
Color palette:
- Neon Radar Green: #00ff66
- Dark Optic Green: #059669
- Light Armor Grey: #829482
- Mid Armor Grey: #384538
- Dark Armor Grey: #1c221c
- Deep Cockpit Black: #0a0d0a
- Pitch Black: #000000

Zero smooth gradients. All crisp edges.
"""
import os

MECHA_HALF_GRID = [
    "                      ", # 0
    "         L            ", # 1: V-fin tip
    "        LMW           ", # 2
    "       LMMD           ", # 3
    "      LMMD            ", # 4
    "     LMMD             ", # 5
    "    LMMD       K      ", # 6: Top antenna & center crest
    "   LMMD       KGK     ", # 7: Green camera optic
    "  LMMD       KGGDK    ", # 8
    " LMMD       KDMMDK    ", # 9: Forehead armor
    "LMMD       KDMWMDK    ", # 10
    " KDD      KDMWMDK     ", # 11
    "  KDDK   KDMMMMDK     ", # 12: Eyebrow plate
    "   KDDDKKDMMMMDK      ", # 13
    "    KDMMMMMMMMK       ", # 14: Visor frame
    "    KDDGGGGGGK        ", # 15: Glowing green mecha visor!
    "   KDMMEEEEEEK        ", # 16: Visor lower reflection
    "   KDMMMMMMDDK        ", # 17: Upper mouthplate
    "   KDMKDKKMDDK        ", # 18: Cooling vent slit 1
    "   KDMDMKDMDDK        ", # 19: Vent grille
    "   KDMKDKKMDDK        ", # 20: Cooling vent slit 2
    "   KDMMMMMMDDK        ", # 21: Lower mouthplate
    "    KDMMMMDDK         ", # 22
    "    KDMWMDDK          ", # 23: Chin block
    "     KDMDDK           ", # 24: Chin tip
    "     KDDDK            ", # 25
    "    KDDMDDK           ", # 26: Neck hydraulics
    "   KDMDKDMDDK         ", # 27
    "  KDMMD KDMMEK        ", # 28: Heavy collar plate
    " KDMMD   KDMMEK       ", # 29
    "KDMMMD   KDMMEEK      ", # 30: Shoulder mount
    "KDMWMD    KDMMEEK     ", # 31
    "KDMWMD    KDGGEEK     ", # 32: Green reactor port
    "KDMMMD    KDGGEEK     ", # 33
    "KDDMDD    KDMMEEK     ", # 34
    " KDMD      KDMEK      ", # 35: Chest armor
    "  KK        KKK       ", # 36
    "                      ", # 37
]

PALETTE = {
    'K': '#050805', # Outline black
    'D': '#182018', # Dark armor
    'M': '#323d32', # Mid armor
    'L': '#5e725e', # Light armor
    'W': '#9bb09b', # Armor highlight
    'G': '#00ff66', # Glowing green visor/optics
    'E': '#047857'  # Shadowed green
}

def build_mecha_svg(px=4, ox=0, oy=0):
    rects = []
    for y, row in enumerate(MECHA_HALF_GRID):
        full_row = row[::-1] + row
        for x, ch in enumerate(full_row):
            if ch in PALETTE:
                rects.append(f'<rect x="{ox + x * px}" y="{oy + y * px}" width="{px}" height="{px}" fill="{PALETTE[ch]}"/>')
    return "".join(rects)

def generate_avatar():
    size = 200
    px = 4
    # Mecha sprite is 44 wide x 38 high -> 44*4 = 176, 38*4 = 152
    ox = (size - 44 * px) // 2 # 12
    oy = (size - 38 * px) // 2 # 24
    
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="{size}" height="{size}" shape-rendering="crispEdges">',
        f'<rect width="{size}" height="{size}" fill="#0a0d0a"/>',
        # Outer pixel border (grey & green)
        f'<rect x="2" y="2" width="{size - 4}" height="{size - 4}" fill="none" stroke="#222b22" stroke-width="2"/>',
        f'<rect x="6" y="6" width="{size - 12}" height="{size - 12}" fill="none" stroke="#00ff66" stroke-width="1" stroke-dasharray="8 4"/>',
        # Mecha HUD corner brackets
        '<rect x="10" y="10" width="12" height="2" fill="#00ff66"/>',
        '<rect x="10" y="10" width="2" height="12" fill="#00ff66"/>',
        '<rect x="178" y="10" width="12" height="2" fill="#00ff66"/>',
        '<rect x="188" y="10" width="2" height="12" fill="#00ff66"/>',
        '<rect x="10" y="188" width="12" height="2" fill="#00ff66"/>',
        '<rect x="10" y="178" width="2" height="12" fill="#00ff66"/>',
        '<rect x="178" y="188" width="12" height="2" fill="#00ff66"/>',
        '<rect x="188" y="178" width="2" height="12" fill="#00ff66"/>',
        # HUD text labels
        '<text x="14" y="20" font-family="\'Courier New\', monospace" font-size="8" font-weight="bold" fill="#829482">機動//01</text>',
        '<text x="140" y="20" font-family="\'Courier New\', monospace" font-size="8" font-weight="bold" fill="#00ff66">TARGET_LOCK</text>',
        '<text x="14" y="185" font-family="\'Courier New\', monospace" font-size="8" font-weight="bold" fill="#00ff66">ALI.SYS</text>',
        '<text x="140" y="185" font-family="\'Courier New\', monospace" font-size="8" font-weight="bold" fill="#829482">BCIT//NED</text>',
        # The Mecha Sprite
        build_mecha_svg(px=px, ox=ox, oy=oy + 2),
        '</svg>'
    ]
    return "\n".join(parts)

def generate_header():
    w, h = 820, 160
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}" shape-rendering="crispEdges">',
        f'<rect width="{w}" height="{h}" fill="#0a0d0a"/>',
        # Outer pixel border
        f'<rect x="2" y="2" width="{w-4}" height="{h-4}" fill="none" stroke="#222b22" stroke-width="2"/>',
        f'<rect x="6" y="6" width="{w-12}" height="{h-12}" fill="none" stroke="#384538" stroke-width="1"/>',
    ]
    
    # Pixelated hazard stripes along top and bottom (pure green/black blocks, no smooth gradients!)
    for x in range(12, w - 12, 16):
        parts.append(f'<rect x="{x}" y="8" width="8" height="4" fill="#00ff66"/>')
        parts.append(f'<rect x="{x + 8}" y="8" width="8" height="4" fill="#182018"/>')
        parts.append(f'<rect x="{x}" y="{h-12}" width="8" height="4" fill="#182018"/>')
        parts.append(f'<rect x="{x + 8}" y="{h-12}" width="8" height="4" fill="#00ff66"/>')
        
    # Left Mecha unit (small pixel sprite)
    parts.append(build_mecha_svg(px=3, ox=30, oy=18))
    # Right Mecha unit (small pixel sprite)
    parts.append(build_mecha_svg(px=3, ox=w - 162, oy=18))
    
    # Center Japanese Typography & HUD
    parts += [
        # Large Katakana 'アリ' (Ali) in crisp pixelated green
        '<text x="410" y="72" font-family="\'Press Start 2P\', \'Courier New\', monospace" font-size="44" font-weight="900" fill="#00ff66" text-anchor="middle" letter-spacing="8">アリ</text>',
        # Kanji subtitle '機動戦士 // サイバーメカ' (Mobile Suit // Cyber Mecha)
        '<text x="410" y="98" font-family="\'Courier New\', monospace" font-size="14" font-weight="bold" fill="#9bb09b" text-anchor="middle" letter-spacing="4">機動戦士 // CYBER MECHA UNIT 01</text>',
        # Telemetry line
        '<text x="410" y="122" font-family="\'Courier New\', monospace" font-size="10" font-weight="bold" fill="#00ff66" text-anchor="middle" letter-spacing="2">[ COCKPIT: ONLINE // SECTOR: KARACHI // OS: BCIT-CORE ]</text>',
        # HUD Crosshair
        '<line x1="390" y1="20" x2="430" y2="20" stroke="#00ff66" stroke-width="1"/>',
        '<line x1="410" y1="14" x2="410" y2="26" stroke="#00ff66" stroke-width="1"/>',
        '</svg>'
    ]
    return "\n".join(parts)

def generate_divider():
    w, h = 820, 20
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}" shape-rendering="crispEdges">',
        f'<rect width="{w}" height="{h}" fill="#0a0d0a"/>',
        # Center rail
        f'<rect x="0" y="9" width="{w}" height="2" fill="#222b22"/>',
        f'<rect x="100" y="8" width="{w - 200}" height="4" fill="#384538"/>',
    ]
    # Pixel hazard pips
    for x in range(120, w - 120, 40):
        parts.append(f'<rect x="{x}" y="7" width="6" height="6" fill="#00ff66"/>')
    # Center Mecha insignia box
    parts += [
        f'<rect x="{w//2 - 40}" y="2" width="80" height="16" fill="#182018" stroke="#00ff66" stroke-width="1"/>',
        f'<text x="{w//2}" y="14" font-family="\'Courier New\', monospace" font-size="9" font-weight="bold" fill="#00ff66" text-anchor="middle" letter-spacing="2">MECHA//01</text>',
        '</svg>'
    ]
    return "\n".join(parts)

def generate_beme_mecha():
    lines = [
        (">be me", "#00ff66"),
        (">CS student in Karachi", "#829482"),
        ('>"just one more commit then sleep"', "#829482"),
        (">it is 4am", "#00ff66"),
        (">the bug was a missing semicolon", "#b8c9b8"),
        (">mfw", "#00ff66")
    ]
    width = 780
    height = 230
    line_height = 25
    start_y = 66
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="{height}" shape-rendering="crispEdges">
  <defs>
    <style>
      .terminal-bg {{ fill: #0a0d0a; stroke: #263326; stroke-width: 2px; }}
      .header-bar {{ fill: #141a14; }}
      .hud-pip {{ fill: #00ff66; }}
      .hud-pip-dim {{ fill: #384538; }}
      .window-title {{ font-family: 'Press Start 2P', 'Courier New', monospace; font-size: 10px; fill: #00ff66; letter-spacing: 1px; }}
      .pixel-text {{
        font-family: 'Press Start 2P', 'VT323', 'Courier New', monospace;
        font-size: 11px;
        letter-spacing: 0.5px;
      }}
      .cursor {{
        font-family: 'Press Start 2P', monospace;
        font-size: 11px;
        fill: #00ff66;
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
  <rect x="2" y="30" width="''' + str(width - 4) + '''" height="1" fill="#00ff66"/>

  <!-- Pips -->
  <rect x="16" y="10" width="8" height="8" class="hud-pip"/>
  <rect x="28" y="10" width="8" height="8" class="hud-pip-dim"/>
  <rect x="40" y="10" width="8" height="8" class="hud-pip-dim"/>

  <!-- Title -->
  <text x="''' + str(width // 2) + '''" y="19" text-anchor="middle" class="window-title">MECHA_LOG // UNIT-01 // >be_me.sh</text>
'''
    for i, (text, col) in enumerate(lines):
        y_pos = start_y + i * line_height
        svg += f'''  <g class="line-{i}">
    <text x="24" y="{y_pos}" fill="{col}" class="pixel-text">{text}</text>
  </g>
'''

    cursor_y = start_y + (len(lines) - 1) * line_height
    svg += f'''  <text x="80" y="{cursor_y}" class="cursor">█</text>
</svg>'''
    return svg

def generate_devnull_mecha():
    items = [
        ("head", "Anonymous 10/31/26(Sat)21:20:11 No.31415926", "#829482", 24),
        ("body", ">ali pushed to main", "#00ff66", 36),
        ("body", '>commit message: "fix"', "#00ff66", 36),
        ("body", '>commit message: "fix2"', "#00ff66", 36),
        ("body", '>commit message: "fix FINAL"', "#00ff66", 36),
        ("body", '>commit message: "fix FINAL real"', "#00ff66", 36),
        ("space", "", "", 0),
        ("head", "Anonymous 10/31/26(Sat)21:20:48 No.31415927", "#829482", 24),
        ("ref", ">>31415926", "#00ff66", 36),
        ("body", "it compiled once on his machine, that's all the QA we need", "#b8c9b8", 36),
        ("space", "", "", 0),
        ("head", "Anonymous 10/31/26(Sat)21:21:30 No.31415928", "#829482", 24),
        ("ref", ">>31415927", "#00ff66", 36),
        ("body", "works on my machine is a valid deployment strategy", "#b8c9b8", 36),
    ]

    width = 780
    height = 370
    start_y = 58
    line_height = 20

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="{height}" shape-rendering="crispEdges">
  <defs>
    <style>
      .terminal-bg {{ fill: #0a0d0a; stroke: #263326; stroke-width: 2px; }}
      .header-bar {{ fill: #141a14; }}
      .hud-pip {{ fill: #00ff66; }}
      .hud-pip-dim {{ fill: #384538; }}
      .window-title {{ font-family: 'Press Start 2P', 'Courier New', monospace; font-size: 10px; fill: #00ff66; letter-spacing: 1px; }}
      .pixel-text {{
        font-family: 'Press Start 2P', 'VT323', 'Courier New', monospace;
        font-size: 10px;
        letter-spacing: 0.3px;
      }}
      .cursor {{
        font-family: 'Press Start 2P', monospace;
        font-size: 10px;
        fill: #00ff66;
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
  <rect x="2" y="30" width="''' + str(width - 4) + '''" height="1" fill="#00ff66"/>

  <!-- Pips -->
  <rect x="16" y="10" width="8" height="8" class="hud-pip"/>
  <rect x="28" y="10" width="8" height="8" class="hud-pip-dim"/>
  <rect x="40" y="10" width="8" height="8" class="hud-pip-dim"/>

  <!-- Title -->
  <text x="''' + str(width // 2) + '''" y="19" text-anchor="middle" class="window-title">BBS://MECHA-NET/SECTOR-KARACHI/31415926</text>
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
        f.write(generate_beme_mecha())
    with open("assets/devnull.svg", "w", encoding="utf-8") as f:
        f.write(generate_devnull_mecha())
    print("Generated all Japanese Cyber Mecha pixel assets in green/grey/black!")
