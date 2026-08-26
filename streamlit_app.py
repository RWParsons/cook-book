"""Rex's Cook Book — Streamlit viewer.

Run with:
    streamlit run streamlit_app.py
"""
import json
import math
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "recipes.json"

st.set_page_config(page_title="Rex's Cook Book", page_icon="🍲", layout="wide")

MACRO_COLORS = {"protein": "#b5562f", "carbs": "#6f8f3e", "fat": "#c99a2e"}


@st.cache_data
def load_recipes():
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def scale_qty(ingredient: dict, factor: float) -> float:
    raw = ingredient["base_qty"] * factor
    if ingredient.get("discrete"):
        return math.ceil(raw - 1e-9)
    if raw < 10:
        return round(raw * 4) / 4  # nearest quarter
    return round(raw / 5) * 5  # nearest 5


def fmt_qty(n: float) -> str:
    if float(n).is_integer():
        return str(int(n))
    return f"{n:.2f}".rstrip("0").rstrip(".")


def volume_message(recipe: dict, factor: float):
    est = recipe.get("estimated_volume_l")
    if not est:
        return None, None
    scaled = est * factor
    max_fill = recipe.get("max_fill_volume_l", 6)
    safe = max_fill * (2 / 3)
    msg = f"Estimated pot volume: **{scaled:.1f}L** of {max_fill}L max fill."
    if scaled > max_fill:
        return "error", msg + " This exceeds the Ninja Foodi's max fill line — cook in batches."
    if scaled > safe:
        return "warning", msg + f" Above the recommended 2/3 fill line ({safe:.1f}L) for foods that expand under pressure — consider batching."
    return "info", msg


def scaled_macros(recipe: dict, calories: float) -> dict:
    base = recipe["macros_per_serve"]
    calorie_factor = calories / base["calories"]
    return {
        "calories": round(calories),
        "protein_g": round(base["protein_g"] * calorie_factor),
        "carbs_g": round(base["carbs_g"] * calorie_factor),
        "fat_g": round(base["fat_g"] * calorie_factor),
        "protein_pct": base["protein_pct"],
        "carbs_pct": base["carbs_pct"],
        "fat_pct": base["fat_pct"],
    }


def macro_bar(macros: dict):
    p, c, f = macros["protein_pct"], macros["carbs_pct"], macros["fat_pct"]
    bar_html = f"""
    <div style="display:flex;height:12px;border-radius:6px;overflow:hidden;margin-bottom:6px;">
      <div style="width:{p}%;background:{MACRO_COLORS['protein']}"></div>
      <div style="width:{c}%;background:{MACRO_COLORS['carbs']}"></div>
      <div style="width:{f}%;background:{MACRO_COLORS['fat']}"></div>
    </div>
    """
    st.markdown(bar_html, unsafe_allow_html=True)
    cols = st.columns(4)
    cols[0].markdown(f":orange[**Protein**] {macros['protein_g']}g ({p}%)")
    cols[1].markdown(f":green[**Carbs**] {macros['carbs_g']}g ({c}%)")
    cols[2].markdown(f":violet[**Fat**] {macros['fat_g']}g ({f}%)")
    cols[3].markdown(f"**{macros['calories']} kcal** / serve")


def ensure_state():
    if "serves" not in st.session_state:
        st.session_state.serves = {}
    if "calories" not in st.session_state:
        st.session_state.calories = {}
    if "shopping_list" not in st.session_state:
        st.session_state.shopping_list = []  # list of dicts


def add_to_shopping_list(recipe: dict, total_factor: float, serves: float):
    for ing in recipe["ingredients"]:
        qty = scale_qty(ing, total_factor)
        match = next(
            (
                item for item in st.session_state.shopping_list
                if item["product"] == ing["product"]
                and item["unit"] == ing["unit"]
                and item["recipe"] == recipe["name"]
            ),
            None,
        )
        if match:
            match["qty"] = float(match["qty"]) + qty
        else:
            st.session_state.shopping_list.append({
                "product": ing["product"],
                "category": ing["category"],
                "qty": qty,
                "unit": ing["unit"],
                "recipe": recipe["name"],
                "checked": False,
            })
    st.toast(f"Added {recipe['name']} ({serves:.0f} serves) to shopping list")


def render_shopping_list():
    st.subheader("Shopping list")
    items = st.session_state.shopping_list
    if not items:
        st.caption("Nothing on your list yet — pick a recipe, set serves, then add it.")
        return

    categories = sorted({item["category"] for item in items})
    for cat in categories:
        st.markdown(f"**{cat}**")
        for idx, item in enumerate(items):
            if item["category"] != cat:
                continue
            key = f"chk_{cat}_{idx}"
            label = f"{item['product']} — {fmt_qty(item['qty'])} {item['unit']}  \n*for {item['recipe']}*"
            checked = st.checkbox(label, value=item["checked"], key=key)
            item["checked"] = checked

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Clear list"):
            st.session_state.shopping_list = []
            st.rerun()
    with col2:
        text_lines = []
        for cat in categories:
            text_lines.append(cat)
            for item in items:
                if item["category"] == cat:
                    text_lines.append(f"  [ ] {item['product']} — {fmt_qty(item['qty'])} {item['unit']}")
        st.download_button(
            "Download list (.txt)",
            data="\n".join(text_lines),
            file_name="grocery_shopping_list.txt",
            mime="text/plain",
        )


def main():
    ensure_state()
    recipes = load_recipes()

    st.title("🍲 Rex's Cook Book")
    st.caption("Beans & lentils · Ninja Foodi (6L) · 40/40/20 macros · Australian grocery shopping lists")

    if not recipes:
        st.info("No recipes yet — add one to data/recipes.json.")
        return

    left, right = st.columns([2.4, 1])

    with left:
        names = [r["name"] for r in recipes]
        selected_name = st.selectbox("Recipe", names)
        recipe = next(r for r in recipes if r["name"] == selected_name)

        serves_col, cal_col = st.columns(2)
        with serves_col:
            default_serves = st.session_state.serves.get(recipe["id"], recipe["base_servings"])
            serves = st.number_input(
                f"Serves (recipe written for {recipe['base_servings']})",
                min_value=1, value=default_serves, step=1,
            )
            st.session_state.serves[recipe["id"]] = serves
        with cal_col:
            base_calories = recipe["macros_per_serve"]["calories"]
            default_calories = st.session_state.calories.get(recipe["id"], base_calories)
            calories = st.number_input(
                f"Calories / serve (recipe written for {base_calories})",
                min_value=1, value=default_calories, step=25,
            )
            st.session_state.calories[recipe["id"]] = calories

        serves_factor = serves / recipe["base_servings"]
        calorie_factor = calories / base_calories
        total_factor = serves_factor * calorie_factor

        total_time = recipe["prep_time_min"] + recipe["cook_time_min"]
        st.caption(f"Total time: {total_time} min")

        level, msg = volume_message(recipe, total_factor)
        if level == "error":
            st.error(msg)
        elif level == "warning":
            st.warning(msg)
        elif level == "info":
            st.caption(msg)

        macro_bar(scaled_macros(recipe, calories))

        st.button(
            "➕ Add current recipe to shopping list",
            on_click=add_to_shopping_list,
            args=(recipe, total_factor, serves),
        )

        st.markdown("### Ingredients")
        for ing in recipe["ingredients"]:
            qty = scale_qty(ing, total_factor)
            st.markdown(f"- {ing['name']} — **{fmt_qty(qty)} {ing['unit']}**")

        st.markdown("### Method")
        for i, step in enumerate(recipe["method"], 1):
            st.markdown(f"{i}. {step}")

    with right:
        render_shopping_list()


if __name__ == "__main__":
    main()
