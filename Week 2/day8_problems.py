import anthropic


client=anthropic.Anthropic(api_key="")

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


