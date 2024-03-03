#!/bin/bash

container_name="keycloak-docker"

# Récupérer le répertoire du script
script_dir=$(dirname "$(readlink -f "$0")")


# Vérifier si le conteneur existe
if docker ps -a --format '{{.Names}}' | grep -q "^$container_name$"; then
    echo "Le conteneur $container_name existe."
    docker start $container_name
    # Ajoutez ici les actions à effectuer si le conteneur existe
    # Par exemple :
    # docker start $container_name
else
    sudo docker run -d --name keycloak-docker -p 8080:8080 -e KEYCLOAK_ADMIN=$1 -e KEYCLOAK_ADMIN_PASSWORD=$2 -v keycloak_save:/opt/keycloak/data quay.io/keycloak/keycloak:23.0.6 
fi

# Ligne à ajouter dans le crontab
cron_line="0 0 * * * $script_dir/mariadb_save.sh"

# Vérifier si la ligne est déjà présente dans le crontab
if ! crontab -l | grep -qF "$cron_line"; then
    # Ajouter la ligne au crontab
    (crontab -l ; echo "$cron_line") | crontab -
    echo "Ligne ajoutée au crontab."
else
    echo "La ligne est déjà présente dans le crontab."
fi
