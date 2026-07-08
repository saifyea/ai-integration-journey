import requests

url="https://official-joke-api.appspot.com/random_joke"

response=requests.get(url)
data=response.json()

print(response)
print(data)
print(f"Setup:{data['setup']}")
print(f"Punchline:{data['punchline']}")


import requests
url="https://randomuser.me/api/"
response=requests.get(url)
data=response.json()
user=data['results'][0]

#print(data)

print(f"Name: {user['name']['first']} {user['name']['last']}")
print(f"email: {user['email']}")
print(f"country: {user['location']['country']}")


