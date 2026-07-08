import anthropic

client = anthropic.Anthropic(api_key="")

response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Python কী? ২ লাইনে বলো।"}
    ]
)

print(response.content[0].text)