with open("README.md", "r", encoding="utf-8") as f:
    text = f.read()

import re
text = re.sub(r'</div>\s*<div align="center">\s*<picture>', '<picture>', text)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(text)
print("Done")
