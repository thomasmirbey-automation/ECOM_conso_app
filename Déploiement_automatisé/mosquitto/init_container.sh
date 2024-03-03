#!/bin/bash

container_name="mosquitto-docker"
# Vérifier si le conteneur existe
if docker ps -a --format '{{.Names}}' | grep -q "^$container_name$"; then
    echo "Le conteneur $container_name existe."
    docker start $container_name
    # Ajoutez ici les actions à effectuer si le conteneur existe
    # Par exemple :
    # docker start $container_name
else
    sudo docker run -d --name mosquitto-docker -p 1883:1883 -v mosquitto_save:/mosquitto/config/ eclipse-mosquitto
    sudo docker cp mosquitto.conf mosquitto-docker:/mosquitto/config/
fi
