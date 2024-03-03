#!/usr/bin/python3

import pymysql
import json

f=open('/script/credentials.json')
data=json.load(f)
# Paramètres de connexion à la base de données
db_config = {
    'host': data['database_ip'],
    'user': data['database_user'],
    'password': data['database_password'],
    'database': data['database'],
}

print(db_config)
# Fonction pour exécuter la procédure stockée
def executer_procedure(valeur, unite, ip):
    try:
        # Connexion à la base de données avec pymysql
        conn = pymysql.connect(**db_config)

        # Création d'un objet curseur
        cursor = conn.cursor()

        # Exécution de la procédure stockée avec des paramètres
        if("'" in unite):
            try:
                unite=unite.replace("'","")
            except:
                pass
        cursor.callproc("ADD_mesure", (valeur, ip, unite ))

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


def add_objet(id_objet,nom_objet,etat_objet,type_objet,ip_objet):
    try:
        # Connexion à la base de données avec pymysql
        conn = pymysql.connect(**db_config)

        # Création d'un objet curseur
        cursor = conn.cursor()

        # Exécution de la procédure stockée avec des paramètres
        cursor.callproc("ADD_objet", (id_objet, nom_objet, etat_objet, type_objet, ip_objet))

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
            
def change_switch_state(state,house_id,switch_ip):
    try:
        # Connexion à la base de données avec pymysql
        conn = pymysql.connect(**db_config)

        # Création d'un objet curseur
        cursor = conn.cursor()

        # Exécution de la procédure stockée avec des paramètres
        cursor.callproc("SET_priseState", (state,house_id,switch_ip))

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
# Exemple d'utilisation
''''
if __name__ == "__main__":
    valeur = 4100  # Remplacez par la valeur souhaitée
    unite = "KW"  # Remplacez par l'unité souhaitée
    ip = "192.168.1.154"  # Remplacez par l'ID de la prise souhaitée

    executer_procedure( valeur, unite, ip)'''
