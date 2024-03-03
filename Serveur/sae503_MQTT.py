#Créer le 27/12/20022
import paho.mqtt.client as mqtt
import time
import ipaddress
from sae503_bdd_set import *
import json
# Cette fonction va permettre de recevoir un reponse CONNACK lorsque le client se connecte au serveur.
def on_connect(client, userdata, flags, rc):
    '''' Cette fonction va permettre de recevoir un reponse CONNACK lorsque le client se connecte au serveur.'''
    print("Connected with result code "+str(rc))

    # Souscrire avec la fonction on_connect() veut dire que si on perd la connexion
    # alors une reconnection après la souscription sera renouvelle.
    # On se connecte donc aux topics des deux gants ci-dessous.
    
        
            
    client.subscribe("test")
 


# Permet de creer un CALLBACK lorsque lon va recevoir un message publie sur le serveur.
def on_message(client, userdata, msg):
    '''Permet de creer un CALLBACK lorsque lon va recevoir un message publie sur le serveur.'''
    if(str(msg.payload).startswith("b")):
        print(msg.topic+" : "+str(msg.payload).split("b")[1])
    else:
        print(msg.topic+" : "+str(msg.payload))
    
    
    if(str(msg.topic)=="mesures/Pinstant"):
        if (str(msg.payload).endswith("W'") or str(msg.payload).endswith("V'") or str(msg.payload).endswith("A'")):
            data1=str(msg.payload).split("b")[1]
            data2=data1.split(" ")
            valeur=data2[0]
            unite=data2[1]
            if("'" in valeur):
                valeur=valeur.replace("'", "")
            executer_procedure(valeur, str(unite), "Onduleur")
            print('Nouvelle mesure')
    elif(str(msg.topic).startswith("mesures/")):
        
        if (str(msg.payload).endswith("W'") or str(msg.payload).endswith("V'") or str(msg.payload).endswith("A'")):
            
                sujet=str(msg.topic).split("/")
                device=sujet[1]
                device_ip=ipaddress.ip_address(device)
                
                data1=str(msg.payload).split("b")[1]
                data2=data1.split(" ")
                valeur=data2[0]
                unite=data2[1]
                if("'" in valeur):
                    valeur=valeur.replace("'", "")
                executer_procedure(valeur, str(unite), device_ip)
                print('Nouvelle mesure')
                
    elif(str(msg.topic).startswith("status/")):

        try:
            
            topic_ip=msg.topic.split("status/")[1]
            ip=ipaddress.ip_address(str(topic_ip))
            message=str(msg.payload).split("b")[1]
            '''if(message.endswith("on")):
                mqtt_publish(client,str(msg.topic),"on")
                
            elif(message.endswith("off")):
                mqtt_publish(client,str(msg.topic),"off")'''
            print(message)
            #on,false or off,true
            if(message.endswith(",true'") or message.endswith(",false'")):
                
                etat=message.split(",")[1]
                if("'" in etat):
                    etat=etat.replace("'", "")
                print(etat,topic_ip)
                change_switch_state(etat,1,str(topic_ip))
                print('Changement d etat')
        except Exception as e:
            print(e)
            pass
    else:
        #au cas ou on veut ajouter du code plus tard
        pass
            
        
            
def mqtt_client(ip,port,timeout):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    #Connexion au serveur MQTT
    try:
        client.connect(ip,port,timeout)
        return client
    except Exception as e:
        print(e)
        return 0
    '''
    #Démarre la boucle de connexion
    client.loop_start()
    print("test")
    client.loop_stop()'''


def mqtt_publish(client,topic,message):
    # Publish a message to the topic "your/topic".
    try:
        client.publish(topic, message)
        return True
    except:
        return False
    
def subscribe_to_topics(client, topic):
    """S'abonne aux topics spécifiés avec l'objet client MQTT."""
    
    client.subscribe(topic)
    
    print(f"topic : {topic}")


f=open('/script/credentials.json')
data=json.load(f)
cli=mqtt_client(data['broker_ip'],int(data['broker_port']),16)

topics=['mesures/#','status/#']
for topic in topics:
    subscribe_to_topics(cli, topic)

cli.loop_start()

