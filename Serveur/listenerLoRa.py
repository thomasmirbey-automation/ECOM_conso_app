#!/usr/bin/python3
import paho.mqtt.client as mqtt
import pymysql
import json
import base64
from sae503_bdd_set import *
from sae503_bdd_get import *
import json

f=open('/script/credentials.json')
data=json.load(f)
# Paramètres de connexion à la base de données
db_config = {
    'host': data['database_ip'],
    'user': data['database_user'],
    'password': data['database_password'],
    'database': data['database'],
}

# Définir les variables
ID = None
adresseIP = None

# Fonction de rappel lors de la réception d'un message MQTT
def on_message(client, userdata, msg):
    global ID, adresseIP

    # Décoder le message
    message = msg.payload.decode("utf-8")
    message_json=json.loads(message)
    try:
        device_id=message_json["end_device_ids"]["device_id"]
        frm_payload=message_json['uplink_message']['frm_payload']
        print(frm_payload)
        frm_payload_decoded=base64.b64decode(frm_payload).decode('utf-8')
        if ('FALSE' in str(execute_stored_procedure("GET_euid",device_id+'-conso'))):
            add_objet(2,device_id+'-conso',"false","CONSO",device_id+'-conso')
            add_objet(2,device_id+'-prod',"false","PROD",device_id+'-prod')
        mesures=frm_payload_decoded.split(',')
        print(mesures)
        executer_procedure(int(mesures[0]),'W',device_id+'-conso')
        executer_procedure(int(mesures[1]),'W',device_id+'-prod')
    except Exception as e:
        print(e)
        pass

# Configurer le client MQTT
client = mqtt.Client()
mqtt_username=data['ttn_user']
mqtt_password = data['ttn_password']
client.username_pw_set(username=mqtt_username, password=mqtt_password)
client.on_message = on_message
# Remplacez "localhost" par l'adresse IP de votre broker MQTT
broker_address = data['ttn_ip']
client.connect(broker_address, int(data['ttn_port']), 60)

# S'abonner au topic "ipDiscover"
client.subscribe("v3/sae601iom@ttn/devices/#")

# Démarrer la boucle MQTT
client.loop_forever()
