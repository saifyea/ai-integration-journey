import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()


client = InferenceClient(
    provider="replicate",
    api_key=os.getenv("HF_TOKEN"),
)

# output is a PIL.Image object
image = client.text_to_image(
    prompt="Bangladesh Map Puzzle educational toy, colorful, white background, product photo",
    model="stabilityai/stable-diffusion-3.5-large",
)



if image:
    image.save("map_puzzle.png")
    print("✅ Saved: map_puzzle.png")


products = [
    {
        "name": "Bangladesh Map Puzzle",
        "prompt": "Bangladesh Map Puzzle wooden toy, "
                  "colorful, educational, white background"
    },
    {
        "name": "Magic Drawing Board",
        "prompt": "LCD magic drawing board for kids, "
                  "colorful, modern, white background"
    },
    {
        "name": "Flash Cards",
        "prompt": "colorful educational flash cards for children, "
                  "bright colors, white background"
    }
]

for product in products:
    print(f"\n📦 {product['name']}")
    image = client.text_to_image(prompt=product["prompt"])

    if image:
        filename = product["name"].replace(" ", "_").lower() + ".png"
        image.save(filename)
        print(f"✅ Saved: {filename}")