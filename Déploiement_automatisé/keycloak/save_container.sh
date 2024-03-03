#!/bin/bash

TIMESTAMP=$(date '+%Y-%m-%d_%H-%M-%S')
BACKUP_DIR="./backup/keycloak_backup_$TIMESTAMP"
mkdir $BACKUP_DIR

sudo docker cp keycloak:/opt/keycloak/data $BACKUP_DIR
