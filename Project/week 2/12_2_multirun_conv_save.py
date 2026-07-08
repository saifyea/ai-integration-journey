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

#to save converstioan in local directory
import json
from datetime import datetime

def save_conversation():
    filename=f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(conversation_history, file,ensure_ascii=False, indent=2)
    
    print(f"✅ Conversation saved: {filename}")


chat("Bangladesh Map Puzzle...")
chat("caption লেখো")

# আগের code এর শেষে যোগ করো
save_conversation()
