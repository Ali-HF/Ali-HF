# -*- coding: utf-8 -*-
"""
Japanese Cyber Mecha Pixel Art Generator
Color palette: Green (#00ff66, #059669), Greys (#181d18, #2b332b, #485448, #829482, #b8c9b8), Black (#0a0d0a)
No smooth gradients anywhere. 100% crisp pixelated aesthetic.
"""

def get_mecha_pixels():
    # 40 wide x 36 high symmetrical pixel art sprite
    # Half-width is 20 pixels (x: 0 to 19, mirrored to 20 to 39)
    # Characters:
    # ' ' = background (transparent)
    # 'K' = black outline (#050805)
    # 'D' = dark armor grey (#1f261f)
    # 'M' = mid armor grey (#384538)
    # 'L' = light armor grey (#6e826e)
    # 'W' = pale highlight grey (#b0c4b0)
    # 'G' = glowing neon green (#00ff66)
    # 'E' = dark optic green (#059669)
    
    half_grid = [
        "                    ", # 0: V-fin tips
        "       L            ", # 1
        "      LMW           ", # 2
        "     LMMD           ", # 3
        "    LMMD            ", # 4
        "   LMMD      K      ", # 5: Top center crest
        "  LMMD      KGK     ", # 6: Top green camera
        " LMMD      KGGDK    ", # 7
        "LMMD      KDMMDK    ", # 8: Forehead
        " KDD     KDMWMDK    ", # 9
        "  KDDK  KDMWMDK     ", # 10
        "   KDDDKDMMMMDK     ", # 11: Eyebrow armor
        "    KDMMMMMMDK      ", # 12
        "    KDDGGGGDK       ", # 13: Neon green mecha visor!
        "   KDMMEEEEKK       ", # 14: Visor shadow
        "   KDMMMMMDDK       ", # 15: Cheek vents
        "   KDMKDKMDDK       ", # 16: Vent slits
        "   KDMDMKMDDK       ", # 17
        "   KDMMMMMDDK       ", # 18: Faceplate
        "    KDMMMDDK        ", # 19
        "    KDMWMDK         ", # 20: Chin plate
        "     KDMDDK         ", # 21: Chin tip
        "     KDDDK          ", # 22
        "    KDDMDDK         ", # 23: Neck hydraulics
        "   KDMDKDMDDK       ", # 24
        "  KDMMD KDMMEK      ", # 25: Collar armor
        " KDMMD   KDMMEK     ", # 26
        "KDMMMD   KDMMEEK    ", # 27: Shoulder pauldrons
        "KDMWMD    KDMMEEK   ", # 28
        "KDMWMD    KDGGEEK   ", # 29: Shoulder green energy ports
        "KDMMMD    KDGGEEK   ", # 30
        "KDDMDD    KDMMEEK   ", # 31
        " KDMD      KDMEK    ", # 32: Chest plate
        "  KK        KKK     ", # 33
        "                    ", # 34
        "                    "  # 35
    ]
    
    full_grid = []
    for row in half_grid:
        left = row[::-1]
        right = row
        full_grid.append(left + right)
    return full_grid

def mecha_to_svg():
    grid = get_mecha_pixels()
    px = 6
    w = len(grid[0]) * px # 40 * 6 = 240
    h = len(grid) * px    # 36 * 6 = 216
    
    colors = {
        'K': '#050805',
        'D': '#182018',
        'M': '#323d32',
        'L': '#5a6e5a',
        'W': '#9eb39e',
        'G': '#00ff66',
        'E': '#047857'
    }
    
    rects = []
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            if ch in colors:
                rects.append(f'<rect x="{x * px}" y="{y * px}" width="{px}" height="{px}" fill="{colors[ch]}"/>')
                
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" shape-rendering="crispEdges">
  <rect width="{w}" height="{h}" fill="#0a0d0a"/>
  <!-- Mecha Pixels -->
  {''.join(rects)}
</svg>'''
    return svg

if __name__ == "__main__":
    with open("assets/mecha.svg", "w", encoding="utf-8") as f:
        f.write(mecha_to_svg())
    print("Generated assets/mecha.svg")
