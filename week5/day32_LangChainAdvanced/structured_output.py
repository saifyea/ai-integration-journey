from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os


load_dotenv()

model = ChatAnthropic(
    model="claude-haiku-4-5-20251001",
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

# ✅ Structured Output Model
class ProductAnalysis(BaseModel):
    product_name: str = Field(description="Product এর নাম")
    price_suggestion: int = Field(description="Suggested price for the product")
    target_audience: str = Field(description="Target customer")
    marketing_tip: str = Field(description="Marketing tip")
    sentiment: str = Field(..., description="The sentiment of the review (positive, negative, neutral)")
    rating: int = Field(description="Market potential 1-10")

#parser
parser = JsonOutputParser(pydantic_object=ProductAnalysis)

#prompt
prompt = ChatPromptTemplate.from_messages([
     ("system", "তুমি F-commerce expert। JSON format এ বাংলায় উত্তর দাও।\n{format_instructions}"),
    ("user", "{product} analyze করো। দাম: {price} টাকা।")
])

prompt = ChatPromptTemplate.from_messages([
    ("system", "তুমি F-commerce expert। শুধুমাত্র JSON format এ উত্তর দাও।\n{format_instructions}"),
    ("user", "{product} analyze করো। দাম: {price} টাকা।")
])

# Chain
chain = prompt | model | parser

print("=== Signle Product Analysis ===")
# Run
result = chain.invoke({
    "product": "Bangladesh Map Puzzle",
    "price": 450,
    "format_instructions": parser.get_format_instructions()
})

print(result)
print(f"\nProduct: {result['product_name']}")
print(f"Rating: {result['rating']}/10")
print(f"Sentiment: {result['sentiment']}")
print(f"Tip: {result['marketing_tip']}")


print("\n\n--- Multiple Products Analysis ---\n")
products = [
    {"product": "Bangladesh Map Puzzle", "price": 450},
    {"product": "Magic Drawing Board", "price": 350},
    {"product": "Flash Cards", "price": 250}
]

print("📊 Product Analysis:")
print("─" * 40)

for p in products:
    result = chain.invoke({
        "product": p["product"],
        "price": p["price"],
        "format_instructions": parser.get_format_instructions()
    })
    print(f"\n🛍️ {result['product_name']}")
    print(f"   💰 Suggested: ৳{result['price_suggestion']}")
    print(f"   ⭐ Rating: {result['rating']}/10")
    print(f"   💡 {result['marketing_tip']}")