import paho.mqtt.client as mqtt

# Configuration
mqtt_broker = "eu1.cloud.thethings.network"
mqtt_port = 1883
mqtt_username = "sae601iom"
mqtt_password = "NNSXS.WDSMKODI6HI6QLYTZX4B25GDQMOWKGUSJUWASWA.XDSXU3IAGJN7XZWFBDA2ZUM3SIMIF25PYDQKOWMLIHMUFEVVHGPA"

# Callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connexion établie au serveur MQTT")
        # Abonnement au sujet de votre périphérique
        client.subscribe("#")
    else:
        print("Impossible de se connecter au serveur MQTT")

def on_message(client, userdata, msg):
    print(f"Message reçu sur le sujet {msg.topic}: {msg.payload.decode()}")

# Configuration du client MQTT
client = mqtt.Client()
client.username_pw_set(username=mqtt_username, password=mqtt_password)
client.on_connect = on_connect
client.on_message = on_message

# Connexion au broker MQTT
client.connect(mqtt_broker, mqtt_port, 60)

# Boucle de mise à jour
client.loop_forever()
