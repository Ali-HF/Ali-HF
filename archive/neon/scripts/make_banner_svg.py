# -*- coding: utf-8 -*-
art = """ █████╗ ██╗     ██╗      ██╗  ██╗███████╗
██╔══██╗██║     ██║      ██║  ██║██╔════╝
███████║██║     ██║█████╗███████║█████╗  
██╔══██║██║     ██║╚════╝██╔══██║██╔══╝  
██║  ██║███████╗██║      ██║  ██║██║     
╚═╝  ╚═╝╚══════╝╚═╝      ╚═╝  ╚═╝╚═╝     """

lines = art.strip("\n").split("\n")
tspans = []
for i, line in enumerate(lines):
    dy = "22" if i > 0 else "0"
    tspans.append(f'<tspan x="50%" dy="{dy}">{line}</tspan>')

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 620 180" width="100%" height="180">
  <defs>
    <linearGradient id="neon" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#05d9e8" />
      <stop offset="50%" stop-color="#ff2a6d" />
      <stop offset="100%" stop-color="#05d9e8" />
    </linearGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="0" stdDeviation="3" flood-color="#ff2a6d" flood-opacity="0.8"/>
    </filter>
  </defs>
  <rect width="100%" height="100%" fill="none"/>
  <text x="50%" y="35" font-family="Consolas, 'Courier New', monospace" font-size="15" font-weight="bold" fill="url(#neon)" text-anchor="middle" filter="url(#glow)" xml:space="preserve">
    {"".join(tspans)}
  </text>
</svg>"""

with open("assets/banner.svg", "w", encoding="utf-8") as f:
    f.write(svg)
print("Generated assets/banner.svg")

