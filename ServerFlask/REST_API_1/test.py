import requests

BASE = "http://127.0.0.1:5000/"

response = requests.put(BASE + "Video/3", {"name": "Szklana pulapka", "views": 1000, "likes": 10})
print(response.json())

response = requests.get(BASE + "Video/10")
print(response.json())

response = requests.patch(BASE + "Video/1", {"name": "Piraci z kalaibow"})
print(response.json())

response = requests.get(BASE + "Video/1")
print(response.json())
