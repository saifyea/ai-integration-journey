import requests

BASE_URL = "http://127.0.0.1:8000"

# Test 1 — Health
print("1. Health Check:")
r = requests.get(f"{BASE_URL}/health")
print(r.json())

# Test 2 — Products
print("\n2. All Products:")
r = requests.get(f"{BASE_URL}/products")
print(r.json())

# Test 3 — Single Product
print("\n3. Product 1:")
r = requests.get(f"{BASE_URL}/products/1")
print(r.json())

# Test 4 — Chat
print("\n4. AI Chat:")
r = requests.post(f"{BASE_URL}/chat", json={
    "message": "Flash Cards এর দাম কত?",
    "user_id": "saif"
})
print(r.json())

# Test 5 — Generate
print("\n5. Generate Content:")
r = requests.post(f"{BASE_URL}/generate", json={
    "product_name": "Flash Cards",
    "price": 250,
    "target": "৩-৬ বছরের শিশু"
})
print(r.json())