from anthropic import Anthropic
from openai import OpenAI
from dotenv import load_dotenv
import os
import time

load_dotenv()

claude = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
#gpt = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))          it will also work but we are using base_url for free token faucet

gpt = OpenAI(
  base_url="https://freetokenfaucet.com/v1",
  api_key=os.getenv("OPENAI_API_KEY"),
)

def ask_claude(question):
    start = time.time()
    response = claude.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        messages=[{"role": "user", "content": question}]
    )
    elapsed = time.time() - start
    return response.content[0].text, elapsed

def ask_gpt(question):
    start = time.time()
    response = gpt.chat.completions.create(
        model="gpt-5.6-terra",
        messages=[{"role": "user", "content": question}]
    )
    elapsed = time.time() - start
    return response.choices[0].message.content, elapsed

# Compare করো
questions = [
    "Python কী? ২ লাইনে বলো।",
    "Bangladesh Map Puzzle এর জন্য Facebook caption লেখো।",
    "RAG system কী?"
]

print("=" * 60)
print("Claude vs GPT-4o-mini Comparison")
print("=" * 60)

for q in questions:
    print(f"\n❓ {q}")
    print("─" * 40)

    claude_ans, claude_time = ask_claude(q)
    print(f"🤖 Claude ({claude_time:.2f}s):")
    print(claude_ans)

    gpt_ans, gpt_time = ask_gpt(q)
    print(f"\n🟢 GPT ({gpt_time:.2f}s):")
    print(gpt_ans)
    print("─" * 40)