import anthropic
from dotenv import load_dotenv
import os

load_dotenv()
api_key=os.getenv("ANTHROPIC_API_KEY")

client=anthropic.Anthropic(api_key=api_key)

response=client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=200,
    messages=[{"role":"user", "content":".env ফাইল সম্পর্কে ১ লাইনে বল"}]
)

print(response.content[0].text)