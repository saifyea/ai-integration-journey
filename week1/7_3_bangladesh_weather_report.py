"""
নাম: bangladesh_weather_report

৩টা বাংলাদেশী শহরের weather বের করো এবং
সুন্দর করে report বানাও:

Dhaka:      23.81, 90.41
Chittagong: 22.34, 91.83
Sylhet:     24.90, 91.87

Output:
🌦️ Bangladesh Weather Report
─────────────────────────────
Dhaka      → 31°C, Wind: 12 km/h
Chittagong → 29°C, Wind: 15 km/h
Sylhet     → 27°C, Wind: 8 km/h
─────────────────────────────
সবচেয়ে গরম: Dhaka 🔥
****এটা সবচেয়ে কঠিন — সব কিছু একসাথে: Function, Dictionary, Loop, Max finder!****
"""

import requests

def get_weather(latitude, longitude):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
    response = requests.get(url)
    data = response.json()
    return data


# Step 1 — শহরের তথ্য
cities = [
    {"name": "Dhaka", "lat": 23.81, "lon": 90.41},
    {"name": "Chittagong", "lat": 22.34, "lon": 91.83},
    {"name": "Sylhet", "lat": 24.90, "lon": 91.87},
]

# Step 2 — Report তৈরি
print("🌦️ Bangladesh Weather Report")
print("─" * 30)

max_temp = -100
hottest_city = ""

for city in cities:
    weather = get_weather(city["lat"], city["lon"])
    temp = weather["current_weather"]["temperature"]
    wind = weather["current_weather"]["windspeed"]

    print(f"{city['name']} → {temp}°C, Wind: {wind} km/h")

    if temp > max_temp:
        max_temp = temp
        hottest_city = city["name"]

# Step 3 — Summary
print("─" * 30)
print(f"সবচেয়ে গরম: {hottest_city} 🔥")