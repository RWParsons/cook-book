# Grocery aisle categories

Use these as the `category` value on each ingredient, so the shopping list on the site groups items the way they're actually laid out in a major Australian supermarket (Coles is the sourcing reference for realism, but this never appears on the site — see naming rule below). Stick to this exact set of strings for consistency across recipes.

- **Fruit & Veg** — fresh produce, herbs, garlic, ginger, onions, citrus.
- **Meat & Seafood** — fresh/raw chicken, beef, pork, fish, seafood.
- **Deli** — sliced meats, fresh dips, olives, deli cheese.
- **Dairy, Eggs & Fridge** — milk, yoghurt, cheese, eggs, fresh stock (chilled), tofu, fresh pasta.
- **Bakery** — bread, wraps, pita.
- **Pantry** — canned goods (legumes, tomatoes, coconut milk), rice, pasta, grains, oils, spices, sauces, stock (shelf-stable), condiments.
- **Freezer** — frozen veg, frozen fruit, frozen fish.
- **Drinks** — juice, soft drink, cordial (rarely needed for savoury recipes).
- **Health Foods** — protein powders, collagen peptides, and similar supplements (health food / vitamins aisle).

## Realistic Australian product naming — without the "Coles" branding

Every ingredient needs a `product` value (see `recipe_schema.json`) that reads like a real, buyable item — sized and worded the way it'd appear at a major Australian grocer like Coles — but the site never labels anything "Coles". So:

- **Store-brand items**: use the plain product description, no retailer prefix. `Coles Brown Onions` → `Brown Onions`. `Coles Ground Cumin` → `Ground Cumin`.
- **Genuinely branded products**: keep the real third-party brand name — that's not store branding, and it's accurate/useful. `SunRice Basmati Rice 1kg`, `Massel Salt Reduced Chicken Style Liquid Stock 1L`, `Keen's Curry Powder 100g`, `Ayam Coconut Milk Light 270mL` all stay as-is.

| Ingredient type | Example `product` value |
|---|---|
| Chicken breast/thigh | `RSPCA Approved Chicken Thigh Fillets` |
| Canned lentils/chickpeas/beans | `Brown Lentils 400g`, `Chick Peas 400g`, `Red Kidney Beans 400g` |
| Canned tomatoes | `Crushed Tomatoes 400g` |
| Coconut milk | `Ayam Coconut Milk Light 270mL` |
| Rice | `SunRice Basmati Rice 1kg` |
| Liquid stock | `Massel Salt Reduced Chicken Style Liquid Stock 1L` |
| Curry powder/paste | `Keen's Curry Powder 100g`, `Valcom Thai Red Curry Paste 235g` |
| Ground spices | `Ground Turmeric`, `Ground Cumin` |
| Olive oil | `Extra Virgin Olive Oil 500mL` |
| Fresh greens | `Baby Spinach 120g` |
| Herbs | `Coriander Bunch` |
| Onion/garlic/ginger | `Brown Onions`, `Garlic`, `Ginger` |
| Citrus | `Limes`, `Lemons` |
| Unflavoured collagen peptides | `Bare Blends Beef Collagen Peptides 300g` |
| Pasta | `San Remo Whole Wheat Spaghetti 500g` |

If unsure of an exact pack size, use a plausible common one (400g cans for legumes/tomatoes, 1kg for rice, 1L for stock) rather than leaving it vague — it should read like a real shopping list.
