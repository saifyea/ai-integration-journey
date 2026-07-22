import anthropic
from anthropic import Anthropic
from dotenv import load_dotenv
import os
load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
conversation_memory=[]

while True:
    user_input=input("You:")

    conversation_memory.append({
        "role":"user",
        "content":user_input
    })

    if user_input=="quit":
        print("allah hafez")
        break
    if user_input=="":
        print("kisu likhte hobe")
        continue


    response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=500,
            system="তুমি একজন বাংলাদেশী F-commerce expert। বাংলায় উত্তর দাও।",
            messages=conversation_memory
        )
    ai_response=response.content[0].text
    conversation_memory.append({
        "role":"assistant",
        "content":ai_response
    })

    print(ai_response)
    print(len(conversation_memory))


