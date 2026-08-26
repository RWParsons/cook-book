"""Sync data/recipes.json into the embedded <script id="recipe-data"> block in site/index.html.

The HTML viewer embeds a copy of the recipe data so it can be opened directly
(double-click) without hitting browser CORS restrictions on local fetch() calls.
Run this after editing data/recipes.json:

    python scripts/sync_recipe_data.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "recipes.json"
HTML_FILE = ROOT / "site" / "index.html"

MARKER = re.compile(
    r'(<script id="recipe-data" type="application/json">\n)(.*?)(\n</script>)',
    re.DOTALL,
)


def main() -> None:
    recipes = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    payload = json.dumps(recipes, indent=2, ensure_ascii=False)

    html = HTML_FILE.read_text(encoding="utf-8")
    match = MARKER.search(html)
    if not match:
        raise SystemExit(
            f'Could not find <script id="recipe-data"> block in {HTML_FILE}'
        )

    new_html = html[: match.start()] + match.group(1) + payload + match.group(3) + html[match.end():]
    HTML_FILE.write_text(new_html, encoding="utf-8")
    print(f"Synced {len(recipes)} recipe(s) from {DATA_FILE.relative_to(ROOT)} into {HTML_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
