#!/bin/bash

container_name="mariadb-docker"
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
    echo "Le conteneur $container_name n'existe pas."
    # Ajoutez ici les actions à effectuer si le conteneur n'existe pas
    docker run -d --name mariadb-docker -e MYSQL_ROOT_PASSWORD=$2 -p 3306:3306 -v mariadb_save:/var/lib/mysql mariadb 
    docker exec mariadb-docker sh -c "apt update"
    docker exec mariadb-docker sh -c "apt install -y mysql-client"
    #docker cp ddb.sql mariadb-docker:/ddb.sql
    #docker cp procedures.sql mariadb-docker:/procedures.sql
    docker exec -it mariadb-docker bash -c "echo 'CREATE DATABASE ecomddb;' | mysql -uroot -p$2"
    docker exec -i mariadb-docker mysql -uroot -p$2 -D ecomddb < "$script_dir/ddb.sql"
    docker exec -i mariadb-docker mysql -uroot -p$2 -e "RENAME USER 'root'@'localhost' TO '$1'@'localhost';"

     #docker exec -i mariadb-docker mysql -uroot -p"tpRT9025" -D ecomddb < procedures.sql

    

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
fi
