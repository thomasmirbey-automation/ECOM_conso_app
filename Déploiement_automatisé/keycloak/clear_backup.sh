#!/bin/bash

# Répertoire à nettoyer
DIRECTORY="./backup"

# Vérifier si le répertoire existe
if [ -d "$DIRECTORY" ]; then
    # Effacer tous les fichiers dans le répertoire
    rm -rf "$DIRECTORY"/*
    echo "Tous les fichiers dans le répertoire $DIRECTORY ont été supprimés."
else
    echo "Le répertoire $DIRECTORY n'existe pas."
fi
