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
        bridge_ip = first_bridge["internalipaddress"]
        bridge_port = first_bridge["port"]

        #Create a dictionary with the bridge information
        bridge_data = {
            "bridge_id": bridge_id,
            "bridge_ip": bridge_ip,
            "bridge_port": bridge_port
        }
        return bridge_data
    else:
        print("No bridges found.")

#Execute if script is ran directly and not imported as module.
if __name__ == "__main__":
    #Welcome!
    print("Welcome to Lumi!")
    sleep(0.5)

    #Grab bridge information as a dictionary
    bridge_data = grab_bridge()
    if len(bridge_data) == 0:
        print("Uh oh, spaghettio. Nothing in the bridge dict.")
    print("Bridge ID:", bridge_data["bridge_id"])
    print("Bridge IP:", bridge_data["bridge_ip"])
    print("Bridge Port:", bridge_data["bridge_port"])
    sleep(0.5)

    #Connect to clip API
    clip_url = "https://" + bridge_data["bridge_ip"] + "/debug/clip.html"
    print("Clip API URL: " + clip_url)
    sleep(0.5)
