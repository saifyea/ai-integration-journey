import anthropic

client=anthropic.Anthropic(api_key="ANTHROPIC_API_KEY")

def product_description_generator(product_name,price,target_customer):

    system_promt=f""" তৃুমি একজন বাংলাদেশেরে সেরা F-Commerce Market Expart!
    তোমার লেখা সবসময়
    -বাংলায় হয়
    -Emoji ব্যবহার কর
    -Emotional এবং Engagin হয়
    -Call to action থাকে """

    user_promt=f"""
    পন্য={product_name}
    দাম={price}
    টার্গেট কাস্টমার={target_customer}

এই পণ্যের জন্য বানাও:
1. Facebook Caption (২-৩ লাইন)
2. Product Description (৫ লাইন)
3. Call to Action (১ লাইন)

    """

    response=client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=500,
        system=system_promt,
        messages=[
            {
                "role":"user",
                "content":user_promt,
            }
        ]
    )
    return response.content[0].text

products=[
    {
        "name":"Bangladesh Puzzle Map",
        "price": 450,
        "target":"শিশুদের অভিভাবক"
    },
    {
        "name":"Magic Drawing Board",
        "price": 350,
        "target":"৫-১০ বছরের শিশু"
    },
    {
        "name": "Flash Cards",
        "price": 250,
        "target": "৩-৬ বছরের শিশু"
    }

]

for product in products:
    print("-"*40)
    print(f"🛍️ {product["name"]}--{product["price"]} টাকা")
    print("-"*40)

    content=product_description_generator(
        product_name=product["name"],
        price=product["price"],
        target_customer=product["target"]
    )
    print(content)

#file save kora
with open ("product_content.txt","w",encoding="utf-8") as file:
    