#!/bin/bash

TIMESTAMP=$(date '+%Y-%m-%d_%H-%M-%S')
BACKUP_DIR="./backup/"
BACKUP_FILE="$BACKUP_DIR/mariadb_backup_$TIMESTAMP.sql"

docker exec mariadb-docker mysqldump -u root --password=$1 --single-transaction --routines --databases ecomddb --skip-column-statistics > $BACKUP_FILE
