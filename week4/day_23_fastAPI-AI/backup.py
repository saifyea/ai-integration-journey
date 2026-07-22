
#endpoint উন্নত সার্চ (একাধিক শব্দে):
@app.get("/products/search")
def search_products(name: str):
    """
    Multiple keywords দিয়েও খোঁজে
    """
    search_terms = name.lower().split()  # "flash cards" → ["flash", "cards"]
    
    found_products = []
    for product in PRODUCTS:
        product_name_lower = product["name"].lower()
        # যেকোনো একটি term মিললেই দেখাবে
        if any(term in product_name_lower for term in search_terms):
            found_products.append(product)
    
    return {
        "status": "success" if found_products else "error",
        "count": len(found_products),
        "products": found_products
    }

#  Error handling যোগ করতে পারো:
from fastapi import HTTPException

if not found_products:
    raise HTTPException(status_code=404, detail="Product not found")

# 🔥 নতুন ফিচার: প্রাইস রেঞ্জ দিয়ে সার্চ
@app.get("/products/filter")
def filter_products(min_price: int = 0, max_price: int = 1000):
    filtered = [p for p in PRODUCTS if min_price <= p["price"] <= max_price]
    return {"count": len(filtered), "products": filtered}

#প্রোডাক্ট আপডেট করো (PUT)
@app.put("/products/{product_id}")
def update_product(product_id: int, request: ProductCreate):
    for i, p in enumerate(PRODUCTS):
        if p["id"] == product_id:
            PRODUCTS[i] = {
                "id": product_id,
                "name": request.name,
                "price": request.price,
                "age": request.age
            }
            return {"status": "success", "product": PRODUCTS[i]}
    raise HTTPException(status_code=404, detail="Product not found")

#প্রোডাক্ট ডিলিট করো (DELETE)
@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    for i, p in enumerate(PRODUCTS):
        if p["id"] == product_id:
            deleted = PRODUCTS.pop(i)
            return {"status": "success", "deleted": deleted}
    raise HTTPException(status_code=404, detail="Product not found")

#Bulk Price Check:
@app.post("/bulk-price-check")
def bulk_price_check(products: list[PriceCheckRequest]):
    results = []
    for p in products:
        # প্রতিটি প্রোডাক্টের জন্য price_check কল করো
        result = price_check(p)
        results.append(result)
    return {"results": results}