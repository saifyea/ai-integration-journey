
"""
নাম: get_weather
Input: latitude, longitude

Open-Meteo API ব্যবহার করো (আজকের মতো)
Return করো: temperature, windspeed

তিনটা শহরের weather বের করো:
- Dhaka: 23.81, 90.41
- London: 51.51, -0.13
- New York: 40.71, -74.01
"""
import requests

def get_weather(latitude,longitude):
   
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
    response = requests.get(url)
    data = response.json()
    return data

print("-"*40,"output problem 3","-"*35)
Dhaka=get_weather(23.81, 90.41)
London=get_weather(51.51, -0.13)
New_York=get_weather(40.71, -74.01)
print(f"Information of Dhaka, Temperature:{Dhaka['current_weather']['temperature']}, Windspeed:{Dhaka['current_weather']['windspeed']}")
print(f"Information of Loondon, Temperature:{London['current_weather']['temperature']}, Windspeed:{London['current_weather']['windspeed']}")
print(f"Information of New_York, Temperature:{New_York['current_weather']['temperature']}, Windspeed:{New_York['current_weather']['windspeed']}")
