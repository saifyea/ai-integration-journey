# তোমার নিজের product এর
# competitor price monitor বানাবো

import requests
from bs4 import BeautifulSoup
from anthropic import Anthropic
from dotenv import load_dotenv
import os
import json
from datetime import datetime

load_dotenv()
client=Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# তোমার products
my_products=[
    {"name": "Bangladesh Map Puzzle", "my_price": 450},
    {"name": "Magic Drawing Board", "my_price": 350},
    {"name": "Flash Cards", "my_price": 250}
]

# Simulate competitor prices
# (Real scraping এ actual URL থেকে নেবে)

competitor_data="""
Competitor A:
- Map Puzzle: 500 টাকা
- Drawing Board: 320 টাকা
- Flash Cards: 280 টাকা

Competitor B:
- Map Puzzle: 420 টাকা
- Drawing Board: 380 টাকা
- Flash Cards: 230 টাকা
"""

my_price_text="\n".join([
     f"- {p['name']}: {p['my_price']} টাকা"
    for p in my_products
])

print("🔍 Price Analysis:")
print("─" * 40)

response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=600,
    system="তুমি একজন e-commerce pricing expert। বাংলায় practical advice দাও।",
    messages=[{
        "role": "user",
        "content": f"""আমার দাম:
{my_price_text}

Competitor দাম:
{competitor_data}

আমাকে বলো:
1. কোন product এ আমি বেশি দাম নিচ্ছি?
2. কোন product এ কম দাম নিচ্ছি?
3. Pricing strategy কী হওয়া উচিত?
4. কোন product এ সবচেয়ে বেশি profit margin আছে?"""
    }]
)

print(response.content[0].text)

# Save result
result = {
    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "analysis": response.content[0].text
}

with open(f"price_analysis_{result['date']}.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"\n✅ Analysis saved to price_analysis_{result['date']}.json")

"""
import pandas as pd
file_safe_date = datetime.now().strftime("%Y-%m-%d_%H-%M")
# Convert and save data
file_name = f"price_analysis_{file_safe_date}.xlsx"
df = pd.DataFrame([result])
df.to_excel(file_name, index=False, engine="openpyxl")

print(f"\nSuccessfully saved to: {file_name}")"""