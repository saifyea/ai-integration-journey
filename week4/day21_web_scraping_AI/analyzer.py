import requests
from bs4 import BeautifulSoup
from anthropic import Anthropic
from dotenv import load_dotenv
import os

load_dotenv()
client=Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Step 1 — Data Scrape করো
url = "https://books.toscrape.com"
reponse=requests.get(url)
soup=BeautifulSoup(reponse.text,"lxml")
books=soup.find_all("article",class_="product_pod")

# Step 2 — Data তৈরি করো
book_data=[]
for book in books[:10]:
    title=book.find("h3").find("a")["title"]
    price=book.find("p",class_="price_color").text
    price = price.encode("ascii", "ignore").decode()
    rating=book.find("p",class_="star-rating")["class"][1]
    book_data.append({
        "title": title,
        "price": price,
        "rating": rating
    })

# Step 3 — AI কে analyze করতে বলো
data_text="\n".join([
    f"Book:{b['title']}, Price:{b['price']}, Rating:{b['rating']}"
    for b in book_data
])

print("📊 Scraped Data:")
print(data_text)
print("\n🤖 AI Analysis:")

response=client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=500,
    messages=[{
        "role": "user",
        "content": f"""এই book data analyze করো:
    {data_text}
    বলো:
    1. সবচেয়ে সস্তা book কোনটা?
    2. সবচেয়ে ভালো rating কোনটা?
    3. Overall market insight কী?"""
    }]

)

print(response.content[0].text)