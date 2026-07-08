import anthropic
from dotenv import load_dotenv
import os

import json
from datetime import datetime

load_dotenv()

api_key=os.getenv("ANTHROPIC_API_KEY")
client=anthropic.Anthropic(api_key=api_key)

conversation=[]

def chat(user_message):

    conversation.append(
        {"role":"user", "content":user_message}
    )

    response=client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        system="তুমি একজন বাংলাদেশী F-commerce expert। বাংলায় উত্তর দাও।",
        messages=conversation
    )

    ai_response=response.content[0].text

    conversation.append(
        {"role":"assistant","content":ai_response}
    )

    return ai_response


def save_conversation():
    filename=f"Conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open (filename,"w", encoding="utf-8") as file:
        json.dump(conversation, file,ensure_ascii=False, indent=2)
    
    print(f"✅ Conversation saved: {filename}")

def fcommerce_assistant():
    print("🛍️ F-commerce AI Assistant চালু!")
    print("'quit' লিখলে বন্ধ হবে, 'save' লিখলে save হবে")
    print("─" * 50)

    while True:
        user_input=input("You: ")

        if user_input.lower()=="quit":
            save_conversation()
            print ("Allah Hafez")
            break

        if user_input.lower()=="save":
            save_conversation()
           # print("Sucessfuly Save")
            continue
        if user_input.strip() == "":
            print("কিছু লেখো!")
            continue
        try:
            response=chat(user_input)
            print (f"AI:{response}")
            print("─" * 50)
        except Exception as e:
            print(f"Error: {e}")

fcommerce_assistant()


