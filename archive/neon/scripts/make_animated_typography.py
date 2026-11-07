# -*- coding: utf-8 -*-
"""Generate animated pixel typography SVGs for '>be me' and '/dev/null/'."""

def generate_beme_svg():
    lines = [
        (">be me", "#72f1b8"),
        (">CS student in Karachi", "#72f1b8"),
        ('>"just one more commit then sleep"', "#72f1b8"),
        (">it is 4am", "#ff2a6d"),
        (">the bug was a missing semicolon", "#f9c80e"),
        (">mfw", "#05d9e8")
    ]
    
    width = 780
    height = 230
    line_height = 25
    start_y = 66
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="{height}">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&amp;family=VT323&amp;display=swap');
      .terminal-bg {{ fill: #0d0221; rx: 6px; stroke: #ff2a6d; stroke-width: 2px; }}
      .header-bar {{ fill: #170936; }}
      .window-btn-red {{ fill: #ff2a6d; }}
      .window-btn-yellow {{ fill: #f9c80e; }}
      .window-btn-cyan {{ fill: #05d9e8; }}
      .window-title {{ font-family: 'Press Start 2P', 'Courier New', monospace; font-size: 10px; fill: #05d9e8; letter-spacing: 1px; }}
      .scanline {{
        fill: none;
        stroke: rgba(5, 217, 232, 0.07);
        stroke-width: 1px;
      }}
      .pixel-text {{
        font-family: 'Press Start 2P', 'VT323', 'Courier New', monospace;
        font-size: 11px;
        letter-spacing: 0.5px;
      }}
      .cursor {{
        font-family: 'Press Start 2P', monospace;
        font-size: 11px;
        fill: #05d9e8;
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

  <!-- Window Frame -->
  <rect x="2" y="2" width="''' + str(width - 4) + '''" height="''' + str(height - 4) + '''" class="terminal-bg"/>
  <rect x="2" y="2" width="''' + str(width - 4) + '''" height="28" class="header-bar" rx="6"/>
  <rect x="2" y="24" width="''' + str(width - 4) + '''" height="6" class="header-bar"/>

  <!-- Window Buttons -->
  <circle cx="20" cy="16" r="5" class="window-btn-red"/>
  <circle cx="36" cy="16" r="5" class="window-btn-yellow"/>
  <circle cx="52" cy="16" r="5" class="window-btn-cyan"/>

  <!-- Window Title -->
  <text x="''' + str(width // 2) + '''" y="19" text-anchor="middle" class="window-title">TERMINAL // >be_me.sh</text>

  <!-- CRT Scanlines -->
'''
    for y in range(35, height - 10, 4):
        svg += f'  <line x1="8" y1="{y}" x2="{width - 8}" y2="{y}" class="scanline"/>\n'

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


def generate_devnull_svg():
    items = [
        # (type, text, color, x_offset)
        ("head", "Anonymous 10/31/26(Sat)21:20:11 No.31415926", "#05d9e8", 24),
        ("body", ">ali pushed to main", "#72f1b8", 36),
        ("body", '>commit message: "fix"', "#72f1b8", 36),
        ("body", '>commit message: "fix2"', "#72f1b8", 36),
        ("body", '>commit message: "fix FINAL"', "#72f1b8", 36),
        ("body", '>commit message: "fix FINAL real"', "#72f1b8", 36),
        ("space", "", "", 0),
        ("head", "Anonymous 10/31/26(Sat)21:20:48 No.31415927", "#ff2a6d", 24),
        ("ref", ">>31415926", "#f9c80e", 36),
        ("body", "it compiled once on his machine, that's all the QA we need", "#ffffff", 36),
        ("space", "", "", 0),
        ("head", "Anonymous 10/31/26(Sat)21:21:30 No.31415928", "#05d9e8", 24),
        ("ref", ">>31415927", "#f9c80e", 36),
        ("body", "works on my machine is a valid deployment strategy", "#ffffff", 36),
    ]

    width = 780
    height = 370
    start_y = 58
    line_height = 20

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="{height}">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&amp;family=VT323&amp;display=swap');
      .terminal-bg {{ fill: #0d0221; rx: 6px; stroke: #05d9e8; stroke-width: 2px; }}
      .header-bar {{ fill: #101c3d; }}
      .window-btn-red {{ fill: #ff2a6d; }}
      .window-btn-yellow {{ fill: #f9c80e; }}
      .window-btn-cyan {{ fill: #05d9e8; }}
      .window-title {{ font-family: 'Press Start 2P', 'Courier New', monospace; font-size: 10px; fill: #ff2a6d; letter-spacing: 1px; }}
      .scanline {{
        fill: none;
        stroke: rgba(255, 42, 109, 0.06);
        stroke-width: 1px;
      }}
      .pixel-text {{
        font-family: 'Press Start 2P', 'VT323', 'Courier New', monospace;
        font-size: 10px;
        letter-spacing: 0.3px;
      }}
      .cursor {{
        font-family: 'Press Start 2P', monospace;
        font-size: 10px;
        fill: #72f1b8;
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

  <!-- Window Frame -->
  <rect x="2" y="2" width="''' + str(width - 4) + '''" height="''' + str(height - 4) + '''" class="terminal-bg"/>
  <rect x="2" y="2" width="''' + str(width - 4) + '''" height="28" class="header-bar" rx="6"/>
  <rect x="2" y="24" width="''' + str(width - 4) + '''" height="6" class="header-bar"/>

  <!-- Window Buttons -->
  <circle cx="20" cy="16" r="5" class="window-btn-red"/>
  <circle cx="36" cy="16" r="5" class="window-btn-yellow"/>
  <circle cx="52" cy="16" r="5" class="window-btn-cyan"/>

  <!-- Window Title -->
  <text x="''' + str(width // 2) + '''" y="19" text-anchor="middle" class="window-title">BBS://dev.null/thread/31415926</text>

  <!-- CRT Scanlines -->
'''
    for y in range(35, height - 10, 4):
        svg += f'  <line x1="8" y1="{y}" x2="{width - 8}" y2="{y}" class="scanline"/>\n'

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

    # Add cursor next to last line
    svg += f'''  <text x="590" y="{y_pos - line_height}" class="cursor">█</text>
</svg>'''
    return svg


if __name__ == "__main__":
    with open('assets/beme.svg', 'w', encoding='utf-8') as f:
        f.write(generate_beme_svg())
    with open('assets/devnull.svg', 'w', encoding='utf-8') as f:
        f.write(generate_devnull_svg())
    print('Generated assets/beme.svg and assets/devnull.svg')

