"""
Complete F-commerce AI Tool
Input:
    → Product নাম
    → দাম
    → Target customer

Output (একসাথে):
    ✅ Facebook Caption
    ✅ Product Description
    ✅ Price Justification
    ✅ 3 Hashtag Set
    ✅ File এ Save
    ✅ Conversation History
"""


import anthropic
import os
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()
import json 

key = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=key)

#Products list
products=[
    {
        "product_name": "Bangladesh Map Puzzle",
        "price": 450,
        "target_customer": "শিশুদের অভিভাবক"
    },
    {
        "product_name": "Magic Drawing Board",
        "price": 350,
        "target_customer": "৫-১০ বছরের শিশু"
    },
    {
        "product_name":  "Flash Cards",
        "price": 250,
        "target_customer": "৩-৬ বছরের শিশু"
    }

    ]
#generate product description, caption, price justification, and hashtags
def generate_product_content(product):
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system=f"""তুমি Saif's Kids Store এর AI marketing expert। সবসময় বাংলায় লেখো। Emoji ব্যবহার করো। Emotional ও engaging content লেখো।""",
        messages=[
            {
            "role": "user", "content": f"""
            পণ্য: {product['product_name']}
             দাম: {product['price']} টাকা
             টার্গেট: {product['target_customer']}
            
            এই পণ্যের জন্য বানাও:
            1. Facebook Caption (৩ লাইন)
            2. Product Description (৫ লাইন)
            3. Price Justification (কেন এই দাম যুক্তিসংগত)
            4. ৫টা Hashtag
            """
            }
        ]
    )
    response_content = response.content[0].text
    return response_content

#content saving function
def save_content_to_file(resutls):
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    filename = f"fcommerce_product_content_{timestamp}.txt"
    
    # Text file এ save
    with open(filename, "w", encoding="utf-8",) as f:
        for item in resutls:
            f.write("=" * 50 + "\n")
            f.write(f"🛍️ {item['product']}\n")
            f.write("=" * 50 + "\n")
            f.write(item['content'] + "\n\n")
            
        
    # JSON file এ save
    with open(f"fcommerce_product_content_{timestamp}.json", "w", encoding="utf-8") as f:
        json.dump(resutls, f, ensure_ascii=False, indent=2)

    print(f"✅ Content saved to {filename} and fcommerce_product_content_{timestamp}.json")

# ✅ Main Program
def main():
    print("🚀 Saif's Kids Store — AI Content Generator")
    print("=" * 50)
    
    results = []

    for product in products:
        print(f"\n⏳ Generating: {product['product_name']}...")

        try:
            content = generate_product_content(product)
            results.append({
                "product": product['product_name'],
                "price": product['price'], 
                "target_customer": product['target_customer'],
                "content": content
                })
            print(f"✅ Done: {product['product_name']}")
            print(content)
            print("-" * 50)
        except Exception as e:
            print(f"❌ Error generating content for {product['product_name']}: {e}")

    # Save করো
    save_content_to_file(results)
    print("\n🎉 সব শেষ! Content ready for posting!")

# Run করো
main()