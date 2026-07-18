from fastapi import FastAPI
from pydantic import BaseModel
from anthropic import Anthropic
from dotenv import load_dotenv
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

@app.get("/products/{product_id}")
def get_product(product_id: int):
    for product in PRODUCTS:
        if product["id"] == product_id:
            return product
    return {"error": "Product পাওয়া যায়নি!"}


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
    
    if found_products:
        return {
            "status": "success",
            "count": len(found_products),
            "products": found_products
        }
    else:
        return {
            "status": "error",
            "message": f"'{name}' নামে কোনো প্রোডাক্ট পাওয়া যায়নি!",
            "suggestions": ["Bangladesh Map Puzzle", "Magic Drawing Board", "Flash Cards"]
        }



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