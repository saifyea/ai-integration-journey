from openai import OpenAI
from dotenv import load_dotenv
import os
import requests

load_dotenv()

client = OpenAI(
  base_url="https://freetokenfaucet.com/v1",
  api_key=os.getenv("OPENAI_API_KEY"),
)

def generate_image(prompt, size="1024x1024"):
    print(f"🎨 Generating: {prompt[:50]}...")

    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size=size,
        quality="standard",
        n=1
    )

    image_url = response.data[0].url
    print(f"✅ Image URL: {image_url[:50]}...")
    return image_url

def save_image(url, filename):
    response = requests.get(url)
    with open(filename, "wb") as f:
        f.write(response.content)
    print(f"✅ Saved: {filename}")

# Test
url = generate_image(
    "Educational Bangladesh Map Puzzle for children, "
    "colorful, wooden toy, white background, "
    "product photography style"
)

save_image(url, "map_puzzle.png")




