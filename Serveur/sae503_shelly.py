import requests
import json

def change_switch_state(shelly_ip,switch_id,state):
    # Replace with your Shelly details
    

    # URL for controlling the switch
    switch_control_url = f"http://{shelly_ip}/rpc/Switch.Set"

    # Payload to turn on the switch
    payload_turn_on = {"id": int(switch_id), "on": bool(state)}

    # Send the POST request
    response = requests.post(switch_control_url, json=payload_turn_on)

    # Print the response
    return(response.json())
    
#print(change_switch_state("192.168.1.128",0,True))
def get_switch_details(shelly_ip,switch_id):
    # Replace with your Shelly details
    

    # URL for controlling the switch
    switch_url = f"http://{shelly_ip}/rpc/shelly.getstatus"

    # Send the POST request
    response = requests.post(switch_url)

    

    # Send the POST request
    response = requests.post(switch_url)

    # Print the response
    return(response.json())

f=open("/script/credentials.json")
data=json.load(f)
shelly_ip = data['shelly_ip']
#print(get_switch_details(shelly_ip,0))
