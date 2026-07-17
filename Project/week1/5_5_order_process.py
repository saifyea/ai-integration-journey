"""
নাম: process_orders
Input: orders (list of dictionaries)


প্রতিটা order validate করো:
- qty > 0 হতে হবে
- product name খালি না হতে হবে
- total = qty × price

সফল হলে  → "✅ Map Puzzle: Total = 2250"
ব্যর্থ হলে → "❌ Magic Board: qty 0 এর বেশি হতে হবে"

শেষে:
- মোট successful orders কতটা
- মোট revenue কত
"""



def process_orders(orders):
    successful=0
    total_revenue=0

    for order in orders:
        try:
            if order["product"]=="":
                raise ValueError("product name খালি না হতে হবে")  
             
            if order["qty"]<=0:
                raise ValueError("Order should not be 0")
    
            total= order["qty"]*order["price"]
            successful+=1
            total_revenue+=total
            print(f"✅ {order['product']}: Total = {total}")

        except ValueError as e:
            print(f"❌ {order['product']}: {e}")
        
    print("Successful Orders:", successful)
    print("Total Revenue:", total_revenue) 


orders = [
    {"product": "Map Puzzle", "qty": 5, "price": 450},
    {"product": "Magic Board", "qty": 2, "price": 350},
    {"product": "Flash Cards", "qty": -1, "price": 250},
    {"product": "", "qty": 3, "price": 200},
]

process_orders(orders)