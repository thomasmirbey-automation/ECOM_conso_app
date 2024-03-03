#!/bin/bash

container_name="keycloak"
# Vérifier si le conteneur existe
if docker ps -a --format '{{.Names}}' | grep -q "^$container_name$"; then
    echo "Le conteneur $container_name existe."
    docker start $container_name
    # Ajoutez ici les actions à effectuer si le conteneur existe
    # Par exemple :
    # docker start $container_name
else
    sudo docker run --name keycloak-docker -p 8080:8080 \
        -e KEYCLOAK_ADMIN= $1 \
        -e KEYCLOAK_ADMIN_PASSWORD= $2 \
        -v keycloak_save:/opt/keycloak/data \
        quay.io/keycloak/keycloak:latest start-dev
fi
