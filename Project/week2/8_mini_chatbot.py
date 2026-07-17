import anthropic

client=anthropic.Anthropic(api_key="ANTHROPIC_API_KEY")

print("🤖 AI Chatbot চালু হয়েছে! ('quit' লিখলে বন্ধ হবে)")
print("-" * 40)

while True:
    user_input = input("তুমি: ")
    
    if user_input.lower() == "quit":
        print("Chatbot বন্ধ হচ্ছে! আল্লাহ হাফেজ 👋")
        break
    
    if user_input == "":
        print("কিছু লেখো!")
        continue
    
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": user_input}
        ]
    )
    
    print(f"AI: {response.content[0].text}")
    print("-" * 40)