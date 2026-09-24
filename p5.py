import requests
import json
import time
import os

os.makedirs("data", exist_ok=True)

API_key = input("Enter your API URL: ")

start_time = time.time()

response = requests.get(API_key)
Status_code = response.status_code
data = response.json()

with open("data/raw.json", "w") as file:
        json.dump(data, file, indent=4)

processed_data = []

for item in data["data"]["data"]:
        processed_data.append({
            "id": item.get("id"),
            "title": item.get("name", {}).get("first")
        })

with open("data/processed.json", "w") as file:
        json.dump(processed_data, file, indent=4)

record = len(processed_data)

end_time = time.time()
response_time = end_time - start_time

print("response_time:", response_time)
print("record:", record)
print("Status_code:", Status_code)
