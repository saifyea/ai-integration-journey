import anthropic
from dotenv import load_dotenv
import os

load_dotenv()

api_key=os.getenv("ANTHROPIC_API_KEY")
client=anthropic.Anthropic(api_key=api_key)

#conversation history
conversation_history=[]

def chat(user_message):
    # conversation shoron rakha hocche
    conversation_history.append(
        {"role":"user", "content":user_message}
    )

    response=client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        system="তুমি একজন বাংলাদেশী F-commerce expert। বাংলায় উত্তর দাও।",
        messages=conversation_history
    )

    #ai response
    ai_response=response.content[0].text
    conversation_history.append(
        {"role":"assistant","content":ai_response}
    )
    return ai_response

# Test করো — AI আগের কথা মনে রাখে কিনা
print(chat("আমার product এর নাম Bangladesh Map Puzzle, দাম ৪৫০ টাকা"))
print("─" * 50)
print(chat("এই product এর জন্য একটা Facebook caption লেখো"))
print("─" * 50)
print(chat("এখন একটু shorter version লেখো"))