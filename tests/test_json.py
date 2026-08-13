import os
import json

print("TEST STARTED")

folder = os.path.join("data", "reports")

print("Creating folder:", folder)

os.makedirs(folder, exist_ok=True)

data = {
    "website": "https://example.com",
    "status": "test"
}

file_path = os.path.join(folder, "raw_scan.json")

print("Writing file:", file_path)

with open(file_path, "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4)

print("JSON CREATED")
print(os.path.abspath(file_path))
