import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

# ✅ Ensure you are using your dedicated Stability AI Platform Key
API_KEY = os.getenv("STABILITY_API_KEY")
if not API_KEY:
    print("❌ Error: STABILITY_API_KEY is missing from your .env file.")
    exit(1)

products = [
    {
        "name": "bangladesh_map",
        "prompt": "Bangladesh Map Puzzle educational toy, colorful, white background, product photo",
    },
    {
        "name": "wooden_alphabet",
        "prompt": "Wooden alphabet blocks toy for children, pastel colors, soft studio lighting",
    },
    {
        "name": "animal_shapes",
        "prompt": "Animal shapes wooden puzzle toy, minimalist design, vibrant colors, clear background",
    },
]

# ✅ Using the stable v2beta generation route for SD3 / SD3.5 models
API_URL = "https://api.stability.ai/v2beta/stable-image/generate/sd3"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "image/*"  # Tells the server to return pure binary image bytes
}

for index, product in enumerate(products):
    filename = f"{product['name']}.png"
    print(f"\n🎨 [{index + 1}/{len(products)}] Generating via Stability AI: {product['prompt'][:40]}...")

    # Set up form payload configurations
    payload = {
        "prompt": product["prompt"],
        "output_format": "png",
        "aspect_ratio": "1:1"  # Options: 1:1, 16:9, 4:3, etc.
    }

    try:
        # ✅ Must pass as data + files due to multipart form-data specification
        response = requests.post(
            API_URL,
            headers=headers,
            files={"none": ""},
            data=payload
        )

        if response.status_code == 200:
            # Save the binary byte response directly as an image file
            with open(filename, "wb") as file:
                file.write(response.content)
            print(f"✅ Successfully saved: {filename}")
        else:
            # Print the detailed JSON failure reasoning from the platform logs
            print(f"❌ Server Error {response.status_code}: {response.json()}")

    except Exception as e:
        print(f"❌ Network/Connection error on {product['name']}: {e}")

    # Standard short sleep to pace loop intervals cleanly
    time.sleep(2)
