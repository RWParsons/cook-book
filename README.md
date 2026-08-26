# Cook Book

Personal recipe collection: legume-forward, high-protein meals cooked in a Ninja Foodi (6L max fill), targeting 40/40/20 (protein/carbs/fat) macros, with Coles Australia shopping lists.

## Structure

```
data/recipes.json          Source of truth — one JSON array of recipes
site/index.html            Standalone recipe book — double-click to open, no server needed
streamlit_app.py           Same recipes, hosted with Streamlit
scripts/sync_recipe_data.py  Copies data/recipes.json into site/index.html's embedded data
.claude/skills/recipe-generator/  Claude Code skill for generating new recipes in-house-style
```

## Adding a recipe

Ask Claude Code to generate one — it will use the `recipe-generator` skill to enforce the house rules (beans/lentils, Ninja Foodi 6L method, 40/40/20 macros, Coles shopping list fields) and append it to `data/recipes.json`. Then sync the standalone HTML copy:

```
python scripts/sync_recipe_data.py
```

(The Streamlit app reads `data/recipes.json` directly, so it doesn't need syncing.)

## Viewing recipes

**Standalone, no install:** open `site/index.html` in a browser. Pick a recipe, adjust serves, and build a shopping list — everything runs client-side and persists to the browser's local storage.

**Streamlit:**

```
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Recipe format

See `.claude/skills/recipe-generator/references/recipe_schema.json` for the full schema, and `data/recipes.json` for a worked example (chicken, lentil & chickpea curry). Key points:

- `base_servings` + `ingredients[].base_qty` define the recipe at its written size; both the HTML and Streamlit viewers scale ingredient quantities from there.
- `macros_per_serve` is fixed per serve regardless of batch size.
- `estimated_volume_l` vs `max_fill_volume_l` drives a fill-line warning when scaling up servings for the Ninja Foodi.
- Ingredients marked `"discrete": true` (cans, onions, limes, etc.) round up when scaled rather than scaling fractionally.
