import os
import json
import time
import logging
import threading
from google.assistant.embedded.v1alpha2 import embedded_assistant_pb2
from google.assistant.embedded.v1alpha2 import embedded_assistant_pb2_grpc
import google.auth.transport.grpc
import google.auth.transport.requests
import google.oauth2.credentials
from tkinter import messagebox

logging.basicConfig(level=logging.DEBUG)

def delay_and_show_message(delay, message):
    time.sleep(delay)
    try:
        messagebox.showinfo("Etat de la prise", message)
    except Exception as e:
        logging.error(f"Erreur lors de l'affichage de la boîte de message : {e}")

def get_credentials():
    # Charger les credentials
    with open(r'credentials.json', 'r') as f:
        cred_data = json.load(f)
    return google.oauth2.credentials.Credentials(token=None, **cred_data)

def establish_grpc_channel(credentials):
    # Établir un canal gRPC sécurisé avec l'API Google Assistant
    grpc_channel = google.auth.transport.grpc.secure_authorized_channel(
        credentials, google.auth.transport.requests.Request(), 'embeddedassistant.googleapis.com')
    return grpc_channel

def create_assistant_client(grpc_channel):
    # Créer un client Google Assistant
    assistant = embedded_assistant_pb2_grpc.EmbeddedAssistantStub(grpc_channel)
    return assistant

def turn_on(device_id, device_model_id):
    # Obtenez les credentials
    credentials = get_credentials()
    
    # Établir un canal gRPC sécurisé avec l'API Google Assistant
    grpc_channel = establish_grpc_channel(credentials)
    
    # Créer un client Google Assistant
    assistant = create_assistant_client(grpc_channel)

    # Configurer la requête de l'assistant pour allumer l'appareil
    text_input = embedded_assistant_pb2.AssistConfig(
        text_query=f"Allume {device_id}",
        audio_out_config=embedded_assistant_pb2.AudioOutConfig(
            encoding='LINEAR16',
            sample_rate_hertz=16000,
            volume_percentage=0  # Mettre à 0 pour ne pas recevoir de réponse audio
        ),
        dialog_state_in=embedded_assistant_pb2.DialogStateIn(
            language_code='fr-FR',
        ),
        device_config=embedded_assistant_pb2.DeviceConfig(
            device_id=device_id,
            device_model_id=device_model_id
        )
    )
    # Faire une requête à l'assistant et recevoir la réponse
    for response in assistant.Assist(iter([embedded_assistant_pb2.AssistRequest(config=text_input)]), None):
        if response.dialog_state_out.supplemental_display_text:
            print("Réponse de l'Assistant Google :", response.dialog_state_out.supplemental_display_text)
            
    threading.Thread(target=delay_and_show_message, args=(1, "La prise est allumée")).start()
    
def turn_off(device_id, device_model_id):
    # Obtenez les credentials
    credentials = get_credentials()
    
    # Établir un canal gRPC sécurisé avec l'API Google Assistant
    grpc_channel = establish_grpc_channel(credentials)
    
    # Créer un client Google Assistant
    assistant = create_assistant_client(grpc_channel)

    # Configurer la requête de l'assistant pour éteindre l'appareil
    text_input = embedded_assistant_pb2.AssistConfig(
        text_query=f"Eteins {device_id}",
        audio_out_config=embedded_assistant_pb2.AudioOutConfig(
            encoding='LINEAR16',
            sample_rate_hertz=16000,
            volume_percentage=0  # Mettre à 0 pour ne pas recevoir de réponse audio
        ),
        dialog_state_in=embedded_assistant_pb2.DialogStateIn(
            language_code='fr-FR',
        ),
        device_config=embedded_assistant_pb2.DeviceConfig(
            device_id=device_id,
            device_model_id=device_model_id
        )
    )
    # Faire une requête à l'assistant et recevoir la réponse
    for response in assistant.Assist(iter([embedded_assistant_pb2.AssistRequest(config=text_input)]), None):
        if response.dialog_state_out.supplemental_display_text:
            print("Réponse de l'Assistant Google :", response.dialog_state_out.supplemental_display_text)
            
    threading.Thread(target=delay_and_show_message, args=(1, "La prise est éteinte")).start()
            



if __name__ == '__main__':
    #check_device_state('002', 'your_device_model_id')
    # Utilisation des fonctions
    turn_on('002', 'your_device_model_id')
    #turn_off('002', 'your_device_model_id')