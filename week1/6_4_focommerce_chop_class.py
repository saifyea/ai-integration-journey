"""
একটা FCommerceShop class বানাও:

__init__: shop_name, products=[]
methods:
    add_product(name, price, stock)
        → products list এ dictionary যোগ করো
    
    show_products()
        → সব product দেখাও
    
    find_product(name)
        → name দিয়ে product খোঁজো
        → না পেলে "Product পাওয়া যায়নি!"

shop = FCommerceShop("Saifuddin's Shop")
shop.add_product("Map Puzzle", 450, 100)
shop.add_product("Magic Board", 350, 50)
shop.show_products()
print(shop.find_product("Map Puzzle"))
print(shop.find_product("Unknown"))
"""

class FCommerceShop:
    def __init__(self,shop_name):
        self.shop_name=shop_name
        self.products=[]
    
    def add_product(self,name,price,stock):
        self.products.append({
                "name":name,
                "price":price,
                "stock":stock
            })


    def show_products(self):
        print(f"Your Product is -> {self.products}")
    
    def find_product(self,name):
        for product in self.products:   
            if product["name"]==name:
                return f" Found Product: {product}"
        return ("Product not found")
  

shop=FCommerceShop("Saif's Shop")
shop.add_product("Map Puzzle", 450, 100)
shop.add_product("Magic Board", 350, 50)
shop.show_products()
print(shop.find_product("Map Puzzle"))
print(shop.find_product("Unknown"))
