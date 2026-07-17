from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from anthropic import Anthropic
from dotenv import load_dotenv
import os
import json
import time

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def scrape_daraz_kitchen():
    print("🌐 Daraz scraping শুরু...")

    # Chrome browser চালু করো
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")        # Background এ চলবে
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        # Daraz kitchen page খোলো
        url = "https://www.daraz.com.bd/kitchen-fixtures/"
        driver.get(url)
        print("✅ Page loaded!")

        # Page load হওয়া পর্যন্ত অপেক্ষা করো
        time.sleep(5)

        # Products খোঁজো
        # তোমার HTML থেকে class names:
        products = driver.find_elements(By.CSS_SELECTOR, "div.Ms6aG")
        print(f"✅ Products found: {len(products)}")

        product_list = []

        for product in products[:len(products)]:  # প্রথম ১০টা
            try:
                # Title
                title_elem = product.find_element(
                    By.CSS_SELECTOR, "div.RfADt a"
                )
                title = title_elem.get_attribute("title")

                # Price
                price_elem = product.find_element(
                    By.CSS_SELECTOR, "span.ooOxS"
                )
                price = price_elem.text

                # Discount
                try:
                    discount_elem = product.find_element(
                        By.CSS_SELECTOR, "span.IcOsH"
                    )
                    discount = discount_elem.text
                except:
                    discount = "N/A"

                # Sold count
                try:
                    sold_elem = product.find_element(
                        By.CSS_SELECTOR, "span._1cEkb span"
                    )
                    sold = sold_elem.text
                except:
                    sold = "N/A"

                # Rating
                try:
                    rating_elem = product.find_element(
                        By.CSS_SELECTOR, "span.qzqFw"
                    )
                    rating = rating_elem.text
                except:
                    rating = "N/A"

                product_list.append({
                    "title": title[:60] + "..." if len(title) > 60 else title,
                    "price": price,
                    "discount": discount,
                    "sold": sold,
                    "rating": rating
                })

                print(f"✅ {title[:40]}... | {price} | {discount}")

            except Exception as e:
                continue

        return product_list

    finally:
        driver.quit()
        print("✅ Browser closed!")


def analyze_with_ai(products):
    if not products:
        print("❌ কোনো product পাওয়া যায়নি!")
        return

    # Data text বানাও
    data_text = "\n".join([
        f"Product: {p['title']}\n"
        f"  Price: {p['price']} | Discount: {p['discount']} | "
        f"Sold: {p['sold']} | Rating: {p['rating']}"
        for p in products
    ])

    print("\n📊 Scraped Products:")
    print(data_text)

    print("\n🤖 AI Analysis:")

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=600,
        system="তুমি Bangladesh e-commerce expert। বাংলায় business insights দাও।",
        messages=[{
            "role": "user",
            "content": f"""Daraz kitchen products data:

{data_text}

আমার জন্য analyze করো:
1. সবচেয়ে popular product কোনটা? (sold count দেখে)
2. সবচেয়ে সস্তা কোনটা?
3. Best value for money কোনটা?
4. Bangladesh kitchen market এ কোন product বেশি demand আছে?
5. নতুন seller হিসেবে কোন product নিয়ে শুরু করা ভালো হবে?"""
        }]
    )

    print(response.content[0].text)

    # Save করো
    result = {
        "products": products,
        "ai_analysis": response.content[0].text
    }

    with open("daraz_kitchen_analysis.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print("\n✅ Saved: daraz_kitchen_analysis.json")


# Run করো
products = scrape_daraz_kitchen()
analyze_with_ai(products)