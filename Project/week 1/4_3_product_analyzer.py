"""
নাম: product_analyzer
Input: products (Dictionary এর List)

products = [
    {"name": "Map Puzzle", "price": 450, "sold": 30},
    {"name": "Magic Board", "price": 350, "sold": 50},
    {"name": "Flash Cards", "price": 250, "sold": 80},
]

কাজ:
- প্রতিটা product এর revenue = price × sold
- সবচেয়ে বেশি revenue কোন product
- মোট revenue কত

Output:
Map Puzzle     → Revenue: 13500
Magic Board    → Revenue: 17500
Flash Cards    → Revenue: 20000
─────────────────────────
Best Product: Flash Cards 🏆
Total Revenue: 51000
"""
print("==========================Output of problem 5==================================")
products = [
    {"name": "Map Puzzle", "price": 450, "sold": 30},
    {"name": "Magic Board", "price": 350, "sold": 50},
    {"name": "Flash Cards", "price": 250, "sold": 80},
]

def product_analyser(produts):
    total_revenue = 0      # মোট revenue
    best_product = ""      # সেরা product
    max_revenue = 0        # সবচেয়ে বেশি revenue

    for product in products:
        revenue =product["price"]*product["sold"]
        total_revenue=total_revenue+revenue
        if max_revenue<=revenue:
            max_revenue=revenue
            best_product=product["name"]
            
        print(product["name"], "→ Revenue:", revenue)

    return total_revenue, best_product

total,best=product_analyser(products)
print("─" * 30)
print("Best Product:",best, "Total Revenue:",total)