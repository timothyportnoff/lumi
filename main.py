from time import sleep
import requests

def grab_bridge():
    # Access the JSON data
    url = "https://discovery.meethue.com/"
    response = requests.get(url)
    data = response.json()

    # Example: Print the first bridge's ID
    if len(data) > 0:
        first_bridge = data[0]
        bridge_id = first_bridge["id"]
        print("Bridge ID:", bridge_id)
    else:
        print("No bridges found.")

if __name__ == "__main__":
    print("Welcome to Lumi!")
    grab_bridge()
