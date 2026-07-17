#custom ai agent for Saif's Kids Store

from langchain.agents import create_agent
#from langchain.agents import AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from dotenv import load_dotenv


import os

load_dotenv()

model = ChatAnthropic(
    model="claude-haiku-4-5-20251001",
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

# ✅ Tool 1 — Price Calculator
@tool
def price_calculator(product_name: str,quantity:int) -> str:
    """Calculate total price for a product and quantity."""
    prices={
        "bangladesh map puzzle": 450,
        "magic drawing board": 350,
        "flash cards": 250
    }
    price = prices.get(product_name.lower())
    if price == 0:
        return f"Product '{product_name}' পাওয়া যায়নি!"

    total = price * int(quantity)
    return f"{product_name}: {price} × {quantity} = {total} টাকা"

# ✅ Tool 2 — Delivery Time
@tool
def delivery_time(location: str) -> str:
    """Get delivery time for a location."""
    if "ঢাকা" in location or "Dhaka" in location:
        return f"{location}: ১-২ দিনের মধ্যে ডেলিভারি"
    else:
        return f"{location}: ৩-৫ দিনের মধ্যে ডেলিভারি"

# ✅ Tool 3 — Product Info
@tool
def product_info(product_name: str) -> str:
    """Get detailed info about a product."""
    products={
        "bangladesh map puzzle": {
            "price": 450,
            "age": "৫-১২ বছর",
            "description": "বাংলাদেশের সম্পূর্ণ মানচিত্র পাজল। ৬৪টি জেলা।"
        },
        "magic drawing board": {
            "price": 350,
            "age": "৩-১০ বছর",
            "description": "LCD magic drawing board। বারবার মুছে আঁকা যায়।"
        },
        "flash cards": {
            "price": 250,
            "age": "৩-৬ বছর",
            "description": "রঙিন শিক্ষামূলক flash cards। ৩০টি কার্ড।"
        }        
    }
    info = products.get(product_name.lower())
    if not info:
        return f"Product পাওয়া যায়নি!"
    
    return f"""
        পণ্য: {product_name}
        দাম: {info['price']} টাকা
        বয়স: {info['age']}
        বিবরণ: {info['description']}
        """
# ✅ Tools List
tools = [price_calculator, delivery_time, product_info]


# Agent বানাও
agent = create_agent(
    model=model,
    tools=tools,
    system_prompt="""তুমি Saif's Kids Store এর AI Assistant। বাংলায় উত্তর দাও।
                সঠিক tool ব্যবহার করে প্রশ্নের উত্তর দাও।"""
)

# Test করো
print("\n🤖 AI Agent Test:")
print("─" * 50)

#কয়েকটি প্রশ্নের উত্তর চাও
questions = [
    "Flash Cards ৫টা কিনলে কত টাকা লাগবে?",
    "চট্টগ্রামে ডেলিভারি কতদিনে পাবো?",
    "Magic Drawing Board সম্পর্কে বিস্তারিত বলো"
]


for q in questions:
    print(f"\n❓ {q}")

    result = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": q
            }
        ]
    })

    print(f"✅ {result['messages'][-1].content}")
    print("─" * 50)


#সরাসরি ইউজার থেকে ইনপুট নাও
print("─" * 50)
print("\n🤖 AI Agent Interactive Mode:")
print("─" * 50)
while True:
    user_input = input("\n❓ আপনার প্রশ্ন লিখুন (বা 'exit' লিখে বের হয়ে যান): ")
    if user_input.lower() == "exit":
        print("AI Agent থেকে বিদায়! 👋")
        break

    result = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": user_input
            }
        ]
    })

    print(f"✅ {result['messages'][-1].content}")
    print("─" * 50)
