---
name: recipe-generator
description: Use this skill when creating a new recipe, converting an existing recipe, or updating data/recipes.json in Rex's cook-book project. Ensures recipes follow house style — beans/lentils included, chicken thigh as the default cut, cooked in a 6L Ninja Foodi, targeting 40/40/20 macros, and paired with an Australian-grocery-realistic shopping list — and are written in the schema the site (site/index.html and streamlit_app.py) expects.
---

# Cook-book recipe generator

Generates recipes for this project's personal cook book: high-protein, legume-forward meals cooked in a Ninja Foodi (6L max fill), hitting a 40/40/20 (protein/carbs/fat) calorie split, with a matching shopping list sourced against what's realistically available at an Australian grocer (Coles). Output is a JSON object appended to `data/recipes.json`, matching the schema every recipe in this repo already uses (see `data/recipes.json` for worked examples).

## Workflow

1. **Clarify the brief** if not already given: protein choice, cuisine/flavour, desired servings (default 6 — good for a few days of meal prep), and any exclusions.
2. **Design the ingredient list** applying the four constraints below.
3. **Compute macros** per serve using the Atwater method (protein/carbs = 4 kcal/g, fat = 9 kcal/g) and iterate on quantities until close to 40/40/20 (±5 percentage points is a good target; note the actual split rather than forcing exact numbers).
4. **Check the 6L fill constraint** and note estimated pot volume.
5. **Write the Ninja Foodi method** as ordered steps (see cook method notes below).
6. **Build the shopping list fields** on each ingredient using realistic Australian product names and aisle categories, without retailer branding (see `references/coles_aisles.md`).
7. **Emit the recipe as JSON** matching `references/recipe_schema.json`, and append it to the array in `data/recipes.json`. Keep the recipe `name` succinct — no appliance/size annotations like "(5L Ninja Foodi)" — and name the cuisine in the title for recognisable regional dishes (e.g. "Indian ...", "Thai ...").
8. **Refresh the standalone HTML viewer** by running `python scripts/sync_recipe_data.py` from the project root, so `site/index.html` picks up the new recipe (it embeds a copy of `data/recipes.json` for opening the file directly without a server).

## The four house constraints

**1. Beans or lentils, always.** Every recipe includes at least one legume (lentils, chickpeas, black beans, kidney beans, cannellini, etc.) as a genuine protein/fibre contributor — not a garnish. Canned, drained/rinsed varieties are the default (fast, no soak time).

**2. Ninja Foodi, 6L max fill.** Default cook method is Sear/Sauté (for aromatics and browning) followed by Pressure Cook, with Air Fry Crisp as an optional finishing step. Estimate total pot volume (liquid + solids, roughly — a can is ~400mL, 800g diced chicken is roughly 800mL, etc.) and record it as `estimated_volume_l`. Keep it comfortably under 6L, and specifically:
   - ≤ 4L (2/3 of max fill) for anything that foams or expands under pressure — legumes, rice, grains, pasta.
   - ≤ 3L (1/2 of max fill) for very foamy foods (e.g. large volumes of dried beans, stock + dairy combos that can foam).
   - If a recipe naturally wants to exceed this, split it into batches or reduce liquid/stock — don't just report a volume over the safe line.

**3. 40/40/20 macros per serve.** Target ~40% of calories from protein, ~40% from carbs, ~20% from fat, per serve. Chicken thigh (not breast) is the house-default cut when a recipe calls for chicken — expect it to run fattier than the target, and use the levers below (trimmed fat elsewhere, collagen) to bring it back toward 40/40/20 rather than swapping back to breast. Practical levers:
   - Trim visible fat off thigh, and go easy on *added* fat elsewhere (oil, coconut milk, ghee, full-fat dairy) to leave headroom for the fat the cut itself brings — a fattier protein source means less budget for cooking fats and rich additions, not more.
   - Carbs come from the legumes plus a grain (rice, pasta, quinoa, etc.) — adjust grain quantity to hit the carb target without overshooting.
   - Fat is the easiest to overshoot — watch oil, coconut milk, cheese, nuts. Use light coconut milk, measure oil in tsp/tbsp rather than "a glug", and trim visible fat.
   - **If protein still falls short after tuning ingredients** (common with fattier cuts like chicken thigh, or dishes built around starchy carbs/legumes where every carb source drags extra carbs along with its protein), stir in **unflavoured collagen peptides**. It's ~90%+ protein by weight with effectively zero carbs or fat, heat-stable (safe in a pressure-cooked or simmered dish), and dissolves clear with no flavour or grain — so it can close a protein gap without disturbing the carb/fat side of the ratio at all. Add it as its own ingredient line and fold the "stir in off the heat until dissolved" step into the method (not a separate notes field — recipe pages only show ingredients and method). A rough guide: ~10–15g (about 1–1.5 tbsp) per serve adds ~9–14g protein for only ~40–55 kcal. Don't reach for it as the first lever — prefer real food (leaner cuts, more legumes) where that alone gets close — but use it whenever the math still won't close. Mention the before/after macro split and why collagen was added directly in the chat reply to the user, not in the recipe data. Worth knowing (and fine to mention in chat): it sets like gelatine when the dish is chilled, so leftovers thicken and may need loosening with extra stock/liquid on reheat. Category for the shopping list: `Health Foods` (see `references/coles_aisles.md`).
   - Show your working: compute total grams of protein/carbs/fat across all ingredients, convert to calories, sum, then divide by servings to get per-serve numbers and percentages. Store the *actual* computed split (e.g. 40/41/19), not a rounded claim of exactly 40/40/20.
   - Nutrition values don't need to be lab-precise — use standard Australian food composition figures (e.g. raw skinless chicken breast ≈ 110 kcal/23g protein/1.5g fat per 100g) and say so is an estimate if asked.

**4. Realistic Australian shopping list, no retailer branding.** Every ingredient needs a `category` (matching an aisle grouping — see `references/coles_aisles.md`) and a `product` (a specific, realistic product name/size you'd actually find at an Australian grocer like Coles — that's the sourcing reference, but the site never says "Coles"). Use the plain product description for store-brand items ("Brown Onions", not "Coles Brown Onions") and real third-party brand names where it's genuinely a branded product ("SunRice Basmati Rice 1kg", "Massel Salt Reduced Chicken Style Liquid Stock 1L"). Mark ingredients bought as discrete units (cans, onions, garlic bulbs, limes, bunches) with `"discrete": true` so the site rounds shopping-list quantities up to whole items when scaling servings, instead of scaling them fractionally.

## No commentary on the recipe page

Recipe pages (both viewers) show only ingredients and method — no extra notes/commentary block. Don't add a `notes` field to the recipe JSON. Anything worth flagging (macro trade-offs, substitutions, storage/reheating quirks, why an ingredient like collagen was added) belongs in the chat reply when presenting the recipe, or folded directly into the relevant method step if it's genuinely needed *while cooking* (e.g. "don't boil hard once the yoghurt is in, or it may split").

## Recipe schema

Full schema and field descriptions: `references/recipe_schema.json`. Key points:
- `base_servings` is the serving count all `base_qty` ingredient amounts are written for.
- `macros_per_serve` is fixed regardless of how many servings are cooked — only ingredient quantities (and `estimated_volume_l`) scale with servings.
- `ingredients[].base_qty` should be a plain number (not a fraction or range) so the site's serving-scaler can multiply it directly.
- `method` is an ordered array of strings, written as Ninja Foodi steps (name the actual function: Sear/Sauté, Pressure Cook, Air Fry Crisp, Slow Cook, Steam).
- `prep_time_min` + `cook_time_min` are summed and shown as a single "Total time" on the recipe page, right below the title — `cook_method` and `source` are stored but not displayed there.

## After generating

Once the JSON is appended to `data/recipes.json` and validated (valid JSON, matches schema), run:

```
python scripts/sync_recipe_data.py
```

This copies `data/recipes.json` into the embedded `<script id="recipe-data">` block in `site/index.html` so the file works standalone (double-click to open, no server/CORS issues). The Streamlit app (`streamlit_app.py`) reads `data/recipes.json` directly at runtime, so it needs no sync step.
