"""
নাম: validate_product
Input: product (Dictionary)

product = {
    "name": "Map Puzzle",
    "price": 450,
    "stock": 100
}

Validate করো:
- name খালি হতে পারবে না
- price অবশ্যই 0 এর বেশি হতে হবে
- stock অবশ্যই 0 বা বেশি হতে হবে

সফল হলে  → "Product Valid ✅"
ব্যর্থ হলে → "Error: [কারণ]"

validate_product({"name":"Map Puzzle","price":450,"stock":100})
→ "Product Valid ✅"

validate_product({"name":"","price":450,"stock":100})
→ "Error: name খালি হতে পারবে না!"

validate_product({"name":"Map Puzzle","price":-50,"stock":100})
→ "Error: price 0 এর বেশি হতে হবে!"
"""



def validate_product(product):
    try:
        if product["name"]=="":
            raise ValueError ( "name খালি হতে পারবে না")
         
        if product["price"]<=0:
            raise ValueError ( "অবশ্যই 0 এর বেশি হতে হবে") 
         
        if product["stock"]<0:
             raise ValueError ( "অবশ্যই 0 বা বেশি হতে হবে") 
         
        return "Product Valid ✅"
    
    except ValueError as e:
        return f"Error: {e}"
    
print(validate_product({"name":"Map Puzzle","price":450,"stock":100}))
print(validate_product({"name":"","price":450,"stock":100}))
print(validate_product({"name":"Map Puzzle","price":-50,"stock":100}))

