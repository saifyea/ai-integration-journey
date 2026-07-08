from langchain_anthropic import ChatAnthropic
#from langchain.prompts import ChatPromptTemplate #from promt template
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime
import os
from dotenv import load_dotenv 
load_dotenv()

#basic api call
"""
model=ChatAnthropic(
    model="claude-haiku-4-5-20251001",
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

response=model.invoke("Python কী? ২ লাইনে বলো।")
#print(response.content)
"""
#promt template
model=ChatAnthropic(
    model="claude-haiku-4-5-20251001",
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

#template
prompt1=ChatPromptTemplate.from_messages([
    ("system", "তুমি একজন {role}। বাংলায় উত্তর দাও।"),
    ("user", "{product} এর জন্য {task}")
])

# template use
chain=prompt1|model

#for miltiple product
products = [
    "Bangladesh Map Puzzle",
    "Magic Drawing Board",
    "Flash Cards"
]
for product in products:
    response=chain.invoke({
        "role": "F-commerce marketing expert",
        "product": product,
        "task": "একটা Facebook caption লেখো"
    })

    print(f"\n{product}:")
    print(response.content)
    print("-" * 40)

"""
products = [
    "Bangladesh Map Puzzle",
    "Magic Drawing Board",
    "Flash Cards"
]

for product in products:
    response = chain.invoke({
        "role": "F-commerce marketing expert",
        "product": product,
        "task": "২ লাইনে একটা caption লেখো"
    })
    print(f"\n{product}:")
    print(response.content)
    print("-" * 40)
"""