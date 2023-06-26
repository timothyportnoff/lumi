from time import *
import requests

url = "https://discovery.meethue.com/"

response = requests.get(url)
data = response.json()

print("Accessing JSON")
# Access the JSON data
# Example: Print the first bridge's ID
if len(data) > 0:
    first_bridge = data[0]
    bridge_id = first_bridge["id"]
    print("Bridge ID:", bridge_id)
else:
    print("No bridges found.")
