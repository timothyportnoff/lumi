from time import sleep
import requests
import json

#def set_bulb(bulb_url):
def grab_bridge():
    # Access the JSON data
    url = "https://discovery.meethue.com/"
    response = requests.get(url)
    data = response.json()

    # Example: Print the first bridge's ID
    if len(data) == 0: 
        print("No bridges found.")
        #print("Uh oh, spaghettio. Nothing in the bridge dict.")
    else:#if len(data) > 0: 
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

def print_menu():
    print("Lumi Options:")
    print("1. Authenticate user.")
    print("2. Turn on all lights")
    print("3. Turn off all lights")
    print("4. Turn on one light")
    print("5. Quit")

def get_user_choice():
    while True:
        choice = input("Enter your choice (1-4): ")
        if choice.isdigit() and 1 <= int(choice) <= 5:
            return int(choice)
        else:
            print("Invalid input. Please enter a valid choice.")

#Execute if script is ran directly and not imported as module.
if __name__ == "__main__":
    try:
        #Welcome!
        print("Welcome to Lumi!")
        sleep(0.5)

        #Grab bridge information as a dictionary
        bridge_data = grab_bridge()
        print("Bridge ID:", bridge_data["bridge_id"])
        print("Bridge IP:", bridge_data["bridge_ip"])
        print("Bridge Port:", bridge_data["bridge_port"])
        sleep(0.5)

        #Establish clip API link
        clip_api_url = "https://" + bridge_data["bridge_ip"] + "/debug/clip.html"
        print("Clip API URL: " + clip_api_url)
        sleep(0.5)

        while True:
            print_menu()
            user_choice = get_user_choice()

            if user_choice == 1: # Authenticate user
                print("You chose Option 1")
                #TODO This will only work once the Hue bridge is pressed, so we should do this in a loop that waits for a minute for the user to press the button.
                # Perform actions for Option 1
                # Send a POST request to the Clip Debugger API to grab an authorized user.
                # Define the message body
                message_body = {
                    "devicetype": "my_hue_app#iphone peter"
                }

                # Convert the message body to JSON
                json_body = json.dumps(message_body)

                # Send a POST request to the Clip Debugger API
                response = requests.post(clip_api_url, data=json_body)
                print("response worked?")

                # Check the response status
                if response.status_code == 200:
                    # Print the response content
                    print(response.text)
                else:
                    print("Failed to send POST request. Error code:", response.status_code)
                    continue
                print("Lumi authorized!") 
                #authorized_ID
                sleep(0.5)

            elif user_choice == 2:
                print("You chose Option 2")
                # Perform actions for Option 2
                #response = requests.get(clip_api_url)

            elif user_choice == 3:
                print("You chose Option 3")
                # Perform actions for Option 3

            elif user_choice == 4:
                print("Quitting...")
                break

            print()  # Print a blank line for readability

        print("Program exited.")
    except requests.exceptions.RequestException as e:
        print("Reached exception block in clip post")
        print("An error occurred during the request:", e)






