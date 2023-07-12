from time import sleep
import urllib3
import requests
import json

api_key = ''
client_key= ''

def grab_bridge():
    url = "https://discovery.meethue.com/"
    response = requests.get(url)
    data = response.json()

    if len(data) <= 0: 
        print("No bridges found.")
    else:
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

menu_options = [ "1. Authenticate user.",
                "2. Print user authentication",
                "3. Print all light info",
                "4. Turn on light",
                "5. Turn off light",
                "0. Quit"]

def print_menu():
    print("Lumi Options:")
    for option in menu_options:
        print("\t" + option)

def get_user_choice():
    while True:
        choice = input("Enter your choice (1-5): ")
        if choice.isdigit() and 0 <= int(choice) < len(menu_options):
            return int(choice)
        else:
            print("Invalid input. Please enter a valid choice.")

#Execute if script is ran directly and not imported as module.
if __name__ == "__main__":
    try:
        #Welcome!
        print("Welcome to Lumi!")
        sleep(0.3)

        #FIXME: First off, this is incredibly unsafe. Please remove.
        # Disable InsecureRequestWarning. Supresses the notification we get from not verifying the SSL cert.
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        #Grab bridge information as a dictionary
        bridge_data = grab_bridge()
        # The above ^ isn't working, use saved bridge info just for personal use"

        print("Bridge ID:", bridge_data["bridge_id"])
        print("Bridge IP:", bridge_data["bridge_ip"])
        print("Bridge Port:", bridge_data["bridge_port"])
        sleep(0.3)

        #Establish Connected Lighting Interface Protocol API Link
        clip_api_url = "https://" + bridge_data["bridge_ip"] + "/debug/clip.html"
        print("Clip API URL: " + clip_api_url)
        sleep(0.3)

        while True:
            print_menu()
            user_choice = get_user_choice()

            if user_choice == 1: # Authenticate user
                try: 
                    print("You chose Option 1")
                    #Send message for our application for api_key and client_key 
                    message_body = { "devicetype":"app_name#instance_name", "generateclientkey":True }

                    #This url is the post URL to grab an authorized user
                    url = "https://" + bridge_data["bridge_ip"] + "/api"

                    #Atttempt to send request for max_attempt seconds for the user to press the button.
                    max_attempts = 8
                    for attempts in range(max_attempts):
                        # Send a POST request to the Clip Debugger APU URL with converted JSON message body
                        response = requests.post(url, data=json.dumps(message_body), verify=False)
                        data = response.json()

                        # Check the response status
                        if response.status_code == 200: # Print the response content
                            if "success" in data[0]:
                                print("Authorization Successful! Response: ", response.text) 
                                api_key = data[0]["success"]["username"]
                                client_key = data[0]["success"]["clientkey"]
                                break
                            elif "error" in data[0]:
                                pass
                        if attempts == max_attempts - 1:
                            print("Failed to POST authentication request. Error code:", response.status_code, "Response: ", response.text)
                        sleep(1)
                except requests.exceptions.RequestException as e:
                    print("An error occurred during the POST request in menu option 1:", e)

            elif user_choice == 2:
                print("You chose Option 2")
                print("Api Key: ", api_key)
                print("Client Key", client_key)

            elif user_choice == 3:
                print("You chose Option 3")
                #url = "https://" + bridge_data["bridge_ip"] + "/api" + api_key + "/lights"
                url = "https://" + bridge_data["bridge_ip"] + "/clip/v2/resource/device"
                # response = requests.post(url, data=json_body, verify=False)
                message_body = { "hue-application-key":api_key }
                json_body = json.dumps(message_body)
                # response = requests.get(url, verify = False)
                # print(response)
                # data = response.json()
                # print(data)

            elif user_choice == 4:
                print("You chose Option 4")
                light="250c6c09-b90c-41f6-aec4-9f5e1d871edd" #This specific light is my personal RIGHT HIGH lamp
                url = "https://" + bridge_data["bridge_ip"] + "/clip/v2/resource/light/" + light
                headers = { "hue-application-key": api_key, "Content-Type": "application/json" }
                payload = { "on": { "on": False } }
                
                #Send put request to URL with api_key and JSON converted message 
                response = requests.put(url, headers=headers, data=json.dumps(payload), verify=False)

                #Handle response code
                if response.status_code == 200:
                    print("PUT request successful. Light ",light, "turned on.")
                else:
                    print("PUT request failed. Error code:", response.status_code)

            elif user_choice == 5:
                print("You chose Option 5")
                light="250c6c09-b90c-41f6-aec4-9f5e1d871edd" #This specific light is my personal RIGHT HIGH lamp
                url = "https://" + bridge_data["bridge_ip"] + "/clip/v2/resource/light/" + light
                headers = { "hue-application-key": api_key, "Content-Type": "application/json" }
                payload = { "on": { "on": True } }
                
                #Send put request to URL with api_key and JSON converted message 
                response = requests.put(url, headers=headers, data=json.dumps(payload), verify=False)

                #Handle response code
                if response.status_code == 200:
                    print("PUT request successful. Light ",light, "turned off.")
                else:
                    print("PUT request failed. Error code:", response.status_code)

            elif user_choice == 0:
                print("You chose to exit the program.")
                break

            sleep(0.3) # Sleep so the user thinks the program is working hard
            print()  # Print a blank line for readability

        print("Exiting Program.")
    except json.JSONDecodeError as e:
        print("Error parsing JSON response:", str(e))
    
    except requests.RequestException as e:
        print("An error occurred during the request:", str(e))

    except KeyboardInterrupt:
        # Code to execute when Ctrl+C is pressed
        print("Ctrl+C detected. Exiting...")

