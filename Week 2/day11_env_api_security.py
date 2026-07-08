import anthropic
from dotenv import load_dotenv
import os
# .env file load করো
load_dotenv()

# Key নাও environment থেকে
api_key=os.getenv("ANTHROPIC_API_KEY")

# Client বানাও
client=anthropic.Anthropic(api_key=api_key)

# Test করো
response=client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=200,
    messages=[{"role":"user", "content":".env ফাইল সম্পর্কে ১ লাইনে বল"}]
)

print(response.content[0].text)