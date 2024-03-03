import requests
import json
from tkinter import messagebox

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
    
#print(change_switch_state("192.168.1.128",0,False))
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

def get_switch_state(shelly_ip,switch_id):
    r=get_switch_details(shelly_ip,switch_id)
    try:
        status=r['switch:'+str(switch_id)]['output']
        if status == True:
            messagebox.showinfo("Etat de la prise", "La prise est allumée")
        else:
            messagebox.showinfo("Etat de la prise", "La prise est éteinte")
        return status
    except:
        messagebox.showerror("Erreur de connexion", "Impossible de récupérer le status de la prise")
        return None
        

shelly_ip = "192.168.1.128"
#print(get_switch_details(shelly_ip,0))