#!/usr/bin/python3

import pymysql


import paho.mqtt.client as mqtt
import pymysql

# Paramètres de connexion à la base de données
db_config = {
    'host': '192.168.1.110',
    'user': 'root',
    'password': 'tpRT9025',
    'database': 'ecomddb',
}

# Fonction pour exécuter la procédure stockée
def executer_procedure(id, ip):
    try:
        # Connexion à la base de données avec pymysql
        conn = pymysql.connect(**db_config)

        # Création d'un objet curseur
        cursor = conn.cursor()

        # Exécution de la procédure stockée avec des paramètres
        cursor.callproc("SET_ipObjet", (id, ip))

        # Valider la transaction
        conn.commit()

        print("Procédure exécutée avec succès.")

    except pymysql.Error as err:
        # En cas d'erreur, annuler la transaction
        conn.rollback()
        print(f"Erreur: {err}")

    finally:
        # Fermeture du curseur et de la connexion
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'conn' in locals() and conn is not None:
            conn.close()




# Définir les variables
ID = None
adresseIP = None

# Fonction de rappel lors de la réception d'un message MQTT
def on_message(client, userdata, msg):
    global ID, adresseIP

    # Décoder le message
    message = msg.payload.decode("utf-8")

    # Séparer les valeurs en utilisant la virgule comme séparateur
    id, adresse_ip = message.split("|")

    # Mettre à jour les variables globales
    ID = id
    adresseIP = adresse_ip

    # Afficher les valeurs
    print("ID:", ID)
    print("Adresse IP:", adresseIP)
    print()
    executer_procedure(ID,adresseIP)
# Configurer le client MQTT
client = mqtt.Client()
client.on_message = on_message

# Remplacez "localhost" par l'adresse IP de votre broker MQTT
broker_address = "192.168.1.105"
client.connect(broker_address, 1883, 60)

# S'abonner au topic "ipDiscover"
client.subscribe("ipDiscover")

# Démarrer la boucle MQTT
client.loop_forever()
