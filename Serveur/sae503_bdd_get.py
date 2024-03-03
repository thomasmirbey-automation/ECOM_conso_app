#!/usr/bin/python3
import pymysql
import json

f=open('/script/credentials.json')
data=json.load(f)

# Paramètres de connexion à la base de données
db_config = {
    'host': data["database_ip"],
    'user': data['database_user'],
    'password': data['database_password'],
    'database': data['database'],
}

# Fonction pour exécuter une procédure stockée
def execute_stored_procedure(nomprocedure,arg=None):
    try:
        
        # Connexion à la base de données avec pymysql
        conn = pymysql.connect(**db_config)

        # Création d'un objet curseur
        cursor = conn.cursor()

        # Exécution de la procédure stockée
        if(arg==None):
            cursor.callproc(nomprocedure)
        else:
            arg_tuple = (arg,) if not isinstance(arg, (tuple, list)) else tuple(arg)
            cursor.callproc(nomprocedure, arg_tuple)

        # Récupération des résultats de la procédure stockée
        results = cursor.fetchall()

        # Affichage des résultats
        #print("Résultats de la procédure stockée:")
        return results
        #for row in results:
        #   print(row)

    except pymysql.Error as err:
        print(f"Erreur: {err}")

    finally:
        # Fermeture du curseur et de la connexion
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'conn' in locals() and conn is not None:
            conn.close()
'''
if __name__ == "__main__":
    #print(execute_stored_procedure("GET_maison"))
    var="192.168.1.128,0"
    print(execute_stored_procedure("GET_objetMesure",var))'''
