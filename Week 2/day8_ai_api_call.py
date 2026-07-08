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


def ask_question(question):
    response=client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[
            {"role":"user","content":question}
        ]
    )
    return response.content[0].text

print(ask_question("Python এ for loop এর একটা example দাও"))


# যেকোনো জায়গায় AI যোগ করতে পারো!
def get_ai_response(question):
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[{"role": "user", "content": question}]
    )
    return response.content[0].text

# E-commerce এ ব্যবহার করো
description = get_ai_response("Map Puzzle এর product description লেখো")
print(description)