import math
print(math.sqrt(16))
print(math.pi)

import random
print(random.randint(1,10))

import requests

response = requests.get("https://api.github.com")
data=response.json()

print("Status Code:", response.status_code)
print("Data Type:", type(response.json()))
print(data)              
print(data.keys()) 


import requests
url = "https://api.open-meteo.com/v1/forecast?latitude=23.951944307118232&longitude=90.26715737780714&current_weather=true"
response = requests.get(url)
data = response.json()

print(data)
print("Temperature:", data["current_weather"]["temperature"], "°C")
