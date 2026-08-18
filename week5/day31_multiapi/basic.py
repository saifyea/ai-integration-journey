from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

#gpt = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))          it will also work but we are using base_url for free token faucet

client = OpenAI(
  base_url="https://freetokenfaucet.com/v1",
  api_key=os.getenv("OPENAI_API_KEY"),
)

response = client.chat.completions.create(
    model="gpt-5.6-luna",
    messages=[
        {"role": "user", "content": "Python কী? ২ লাইনে বলো।"}
    ]
)

print(response.choices[0].message.content)

