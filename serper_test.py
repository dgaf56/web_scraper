
#intial test worked
#import os
#import requests

#SERPER_KEY = os.getenv("SERPER_KEY")
#URL = "https://google.serper.dev/images"

#headers = {
#    "X-API-KEY": SERPER_KEY,
#    "Content-Type": "application/json"
#}

#payload = {"q": "cats"}

#response = requests.post(URL, headers=headers, json=payload)

#print("Status:", response.status_code)
#print("Response text:", response.text)   # <-- ADD THIS

#response.raise_for_status()
#data = response.json()

#print(type(data))
#print(data.keys())

#next step

import os
import requests

SERPER_KEY = os.getenv("SERPER_KEY")
URL = "https://google.serper.dev/images"

headers = {"X-API-KEY": SERPER_KEY, "Content-Type": "application/json"}
payload = {"q": "cats"}

response = requests.post(URL, headers=headers, json=payload)
response.raise_for_status()
data = response.json()

images = data["images"]              # list of dictionaries
print("How many images:", len(images))

for img in images:
    print(img["imageUrl"])
