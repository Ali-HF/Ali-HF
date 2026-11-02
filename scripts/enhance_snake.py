# -*- coding: utf-8 -*-
"""
Post-processes the Platane/snk output SVGs:
1. Sets empty tiles (--ce, --c0) to a clear, visible greyish color (#2d333b).
2. Sets contribution dots (--c1 to --c4) to a rich gradient of greens.
3. Styles the snake body segments (.s0, .s1, .s2, .s3) with an actual green gradient!
   - .s0 (head): #aff5b4 (bright pastel mint)
   - .s1 (upper body): #7ee787 (GitHub pastel green)
   - .s2 (lower body): #3fb950 (mid emerald green)
   - .s3 (tail): #238636 (deep forest green)
"""
import glob
import re
import os

def enhance_svg(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Ensure valid hex colors in :root
    # Empty tile: #2d333b (visible greyish)
    # Green gradient dots:
    # c1: #1b4727
    # c2: #2ea043
    # c3: #3fb950
    # c4: #7ee787
    content = re.sub(r'--ce:[^;]+;', '--ce:#2d333b;', content)
    content = re.sub(r'--c0:[^;]+;', '--c0:#2d333b;', content)
    content = re.sub(r'--c1:[^;]+;', '--c1:#1b4727;', content)
    content = re.sub(r'--c2:[^;]+;', '--c2:#2ea043;', content)
    content = re.sub(r'--c3:[^;]+;', '--c3:#3fb950;', content)
    content = re.sub(r'--c4:[^;]+;', '--c4:#7ee787;', content)
    content = re.sub(r'--cb:[^;]+;', '--cb:#30363d;', content)

    # Snake gradient styling
    snake_gradient_css = """
/* Snake green gradient */
.s.s0 { fill: #aff5b4 !important; filter: drop-shadow(0 0 2px #7ee787); }
.s.s1 { fill: #7ee787 !important; }
.s.s2 { fill: #3fb950 !important; }
.s.s3 { fill: #238636 !important; }
"""
    if "/* Snake green gradient */" not in content:
        content = content.replace("</style>", snake_gradient_css + "</style>")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Enhanced {file_path}")

if __name__ == "__main__":
    for p in glob.glob("dist/*.svg"):
        enhance_svg(p)

