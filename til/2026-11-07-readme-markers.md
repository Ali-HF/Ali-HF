# Using HTML comment markers to rewrite a README

Self-updating GitHub profile READMEs—a technique popularized by [Simon Willison](https://simonwillison.net/2020/jul/10/self-updating-profile-readme/)—often need to refresh dynamic content (such as recently pushed repositories, latest blog posts, or daily ASCII art) without blowing away hand-written introductory text.

The cleanest solution is to demarcate dynamic sections using HTML comments:

```markdown
<!-- recent_pushes starts -->
* [my-project](https://github.com/Ali-HF/my-project) - Description (2 days ago)
<!-- recent_pushes ends -->
```

### Why this works

1. **Invisible in rendered output**: HTML comments (`<!-- ... -->`) are valid syntax in GitHub Flavored Markdown (GFM). The Markdown parser ignores them when generating HTML, so visitors never see the markers.
2. **Safe boundaries for automation**: A lightweight script running in GitHub Actions can locate and replace only the text between the start and end markers using a regex:

```python
import re

def replace_chunk(content: str, marker: str, replacement: str) -> str:
    pattern = re.compile(
        rf"<!-- {marker} starts -->.*<!-- {marker} ends -->",
        re.DOTALL,
    )
    chunk = f"<!-- {marker} starts -->\n{replacement.strip()}\n<!-- {marker} ends -->"
    return pattern.sub(chunk, content)
```

3. **Human-friendly**: If an automated script fails (for example, if an external API rate-limits or errors out), the workflow can simply leave the file untouched. The author remains free to edit other parts of the README without interfering with the automated sections.
