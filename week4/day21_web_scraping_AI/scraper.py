import requests
from bs4 import BeautifulSoup

# একটা simple website থেকে data নাও
url = "https://books.toscrape.com"

response=requests.get(url)
soup=BeautifulSoup(response.text,"lxml")

# সব book এর নাম ও দাম বের করো
books=soup.find_all("article",class_="product_pod")

print(f"মোট books: {len(books)}")
print("─" * 40)

for book in books[:5]: # প্রথম ৫টা
    title=book.find("h3").find("a")["title"]
    price=book.find("p",class_="price_color").text
    price = price.encode("ascii", "ignore").decode()
    print(f"📚 {title}")
    print(f"   💰 {price}")
    print("─" * 40)