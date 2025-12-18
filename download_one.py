
#proof/test
#import requests

#url = "https://www.cdc.gov/healthy-pets/media/images/2024/04/Cat-on-couch.jpg"

#r = requests.get(url, timeout=20, headers={"User-Agent": "Mozilla/5.0"})
#r.raise_for_status()

#with open("one.jpg", "wb") as f:
#    f.write(r.content)

#print("Saved one.jpg")

import os
import requests

# 1) Choose a folder name
IMAGE_DIR = "images"

# 2) Create the folder if it doesn't exist
os.makedirs(IMAGE_DIR, exist_ok=True)

# 3) Image URL (one you tested earlier)
url = "https://www.cdc.gov/healthy-pets/media/images/2024/04/Cat-on-couch.jpg"

# 4) Download the image
r = requests.get(url, timeout=20, headers={"User-Agent": "Mozilla/5.0"})
r.raise_for_status()

# 5) Build the full file path safely
file_path = os.path.join(IMAGE_DIR, "one.jpg")

# 6) Save the image bytes
with open(file_path, "wb") as f:
    f.write(r.content)

print(f"Saved {file_path}")
