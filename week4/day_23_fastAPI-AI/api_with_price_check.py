from fastapi import FastAPI
from pydantic import BaseModel
from anthropic import Anthropic
from dotenv import load_dotenv
from typing import Optional #Optional নতুন প্রোডাক্ট যোগ করো
import os

load_dotenv()

app = FastAPI(
    title="Saif's Kids Store AI API",
    description="AI-powered API for Kids Store",
    version="1.0.0"
)

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

PRODUCTS = [
    {"id": 1, "name": "Bangladesh Map Puzzle", "price": 450, "age": "৫-১২ বছর"},
    {"id": 2, "name": "Magic Drawing Board", "price": 350, "age": "৩-১০ বছর"},
    {"id": 3, "name": "Flash Cards", "price": 250, "age": "৩-৬ বছর"}
]

# ✅ Request Models
class ChatRequest(BaseModel):
    message: str
    user_id: str = "default"

class GenerateRequest(BaseModel):
    product_name: str
    price: int
    target: str = "শিশুদের অভিভাবক"

# ✅ নতুন Request Model
class ProductCreate(BaseModel):
    name: str
    price: int
    age: str

class PriceCheckRequest(BaseModel):
    product_name: str
    my_price:int


# ✅ Endpoints
@app.get("/health")
def health_check():
    return {
        "status": "✅ API চলছে!",
        "version": "1.0.0",
        "store": "Saif's Kids Store"
    }

@app.get("/products")
def get_products():
    return {
        "total": len(PRODUCTS),
        "products": PRODUCTS
    }


# 🔍 NEW: Product Search by Name
@app.get("/products/search")
def search_products(name: str):
    """
    নাম দিয়ে প্রোডাক্ট খোঁজে (partial match)
    """
    found_products = []
    for product in PRODUCTS:
        if name.lower() in product["name"].lower():
            found_products.append(product)
            return found_products
    return {"error": "Product পাওয়া যায়নি!"}


@app.get("/products/{product_id}")
def get_product(product_id: int):
    for product in PRODUCTS:
        if product["id"] == product_id:
            return product
    return {"error": "Product পাওয়া যায়নি!"}


@app.post("/chat")
def chat(request: ChatRequest):
    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            system="""তুমি Saif's Kids Store এর AI Assistant।
বাংলায় সংক্ষেপে উত্তর দাও।
Products:
- Bangladesh Map Puzzle: ৪৫০ টাকা
- Magic Drawing Board: ৩৫০ টাকা
- Flash Cards: ২৫০ টাকা""",
            messages=[{
                "role": "user",
                "content": request.message
            }]
        )
        return {
            "user_id": request.user_id,
            "message": request.message,
            "response": response.content[0].text
        }
    except Exception as e:
        return {"error": str(e)}

@app.post("/generate")
def generate_content(request: GenerateRequest):
    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=400,
            system="তুমি F-commerce marketing expert। বাংলায় লেখো।",
            messages=[{
                "role": "user",
                "content": f"""
পণ্য: {request.product_name}
দাম: {request.price} টাকা
টার্গেট: {request.target}

বানাও:
1. Facebook Caption (২ লাইন)
2. Product Description (৩ লাইন)
3. ৩টা Hashtag
"""
            }]
        )
        return {
            "product": request.product_name,
            "price": request.price,
            "content": response.content[0].text
        }
    except Exception as e:
        return {"error": str(e)}
    
@app.post("/products")
def create_product(request:ProductCreate):
    """
    নতুন প্রোডাক্ট যোগ করে
    """
    # নতুন ID জেনারেট করো
    new_id = max([p["id"] for p in PRODUCTS]) + 1 if PRODUCTS else 1
    new_product = {
        "id": new_id,
        "name": request.name,
        "price": request.price,
        "age": request.age
    }
        
    PRODUCTS.append(new_product)
    return {
        "status": "success",
        "message": f"✅ '{request.name}' প্রোডাক্টটি যোগ করা হয়েছে!",
        "product": new_product
    }


@app.post("/price-check")
def price_check(request: PriceCheckRequest):
    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            system="তুমি Bangladesh e-commerce pricing expert। বাংলায় practical advice দাও।",
            messages=[{
                "role": "user",
                "content": f"""
                Product: {request.product_name}
                আমার দাম: {request.my_price} টাকা

                Competitor দাম:
                - Bangladesh Map Puzzle: ৪০০-৫০০ টাকা
                - Magic Drawing Board: ৩০০-৪০০ টাকা
                - Flash Cards: ২০০-৩০০ টাকা

                বলো:
                1. আমার দাম ঠিক আছে?
                2. বেশি নাকি কম?
                3. Suggestion কী?
                """
            }]
        )
        return {
            "product": request.product_name,
            "my_price": request.my_price,
            "analysis": response.content[0].text
        }
    except Exception as e:
        return {"error": str(e)}
    