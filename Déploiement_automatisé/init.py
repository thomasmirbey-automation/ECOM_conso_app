import argparse
import os
#import paramiko
import git 
import shutil
#import subprocess

#############################################  ARG
parser = argparse.ArgumentParser(description='Script avec des arguments facultatifs')

parser.add_argument('-os', type=str, default="Linux", help='The os you use, Linux or Windows', required=False)

#parser.add_argument('--ecom_id', type=str, default="None", help='ECOM id', required=True)
#parser.add_argument('--ecom_password', type=str, default="None", help='ECOM password', required=True)
#parser.add_argument('--ecom_server', type=str, default="None", help='ECOM password', required=True)

parser.add_argument('--service_id', type=str, default="admin", help='ECOM', required=False)
parser.add_argument('--service_password', type=str, default="admin", help='ECOM', required=False)


args = parser.parse_args()
########################################################################################################################

def repertoire_non_vide(chemin_repertoire):
    # Vérifie si le chemin est un répertoire
    if not os.path.isdir(chemin_repertoire):
        raise ValueError("Le chemin spécifié n'est pas un répertoire.")
    
    # Liste le contenu du répertoire
    contenu = os.listdir(chemin_repertoire)
    
    # Retourne True si le répertoire n'est pas vide, sinon False
    return bool(contenu)


def is_line_in_crontab(line):
    try:
        # Ouvre le fichier crontab en mode lecture
        with open('/etc/crontab', 'r') as file:
            # Lit toutes les lignes du fichier
            for l in file:
                # Vérifie si la ligne spécifiée est présente
                if line in l:
                    return True
        return False
    except FileNotFoundError:
        print("Le fichier crontab n'a pas été trouvé.")
        return False
        

def download_github_folder(repo_url, folder_path, destination_path):
    try:
        print('Recuperation dossier github')
        if os.path.exists('temp_repo'):
            shutil.rmtree('temp_repo')

         # Cloner le référentiel GitHub en mémoire
        git.Repo.clone_from(repo_url, 'temp_repo')

         # Supprimer le répertoire de destination s'il existe déjà
        if os.path.exists(destination_path):
            shutil.rmtree(destination_path)

         # Copier le dossier spécifique vers l'emplacement de destination
        shutil.copytree('./temp_repo/' + folder_path, destination_path)

         # Supprimer le référentiel temporaire
        shutil.rmtree('temp_repo')
        print('Dossier github recupere !')
        return destination_path

    except Exception as e:
        print(f"Erreur lors du téléchargement du dossier depuis GitHub: {e}")
        return None

    
def main():
    if (args.os.lower()!='linux'):
        return (args.os+' not supported at the moment')
    args_dict = vars(args)
    print(args_dict)
    os.system('apt install -y docker docker-compose python3')
    
    '''
    directories=['./script','./log']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print('Repertoire cree')
    '''
    #if(args_dict['ecom_id']!='None' and args_dict['ecom_password']!='None' and args_dict['ecom_server']!='None'):
       #scp(args_dict['ecom_id'],args_dict['ecom_password'],args_dict['ecom_server'],'/script','/script')
       
    repo_url ="https://github.com/thomasmirbey-automation/ECOM_Project.git"
    downloaded_folder_path = []
    downloaded_folder_path.append(download_github_folder(repo_url, 'ECOM/Docker', './docker'))
    downloaded_folder_path.append(download_github_folder(repo_url, 'ECOM/Script', './script'))
    downloaded_folder_path.append(download_github_folder(repo_url, 'ECOM/App', './app'))
    


    print(downloaded_folder_path)

    #os.system('pip install requests ipaddress paho.mqtt time datetime meross_iot asyncio pymysql json')
    if repertoire_non_vide('./docker/'):
#         docker_content = os.listdir('./docker')
         for path in os.listdir('./docker'):
             print(path)
             if os.path.exists('./docker/'+path+'/init_container.sh'):
                 print(args_dict['service_id'])
                 print(args_dict['service_password'])
                 print('Lancement du script : ./docker/'+path+'/init_container.sh')
                 #subprocess.run(['sudo', './docker/' + path + '/init_container.sh', args_dict['service_id'], args_dict['service_password']])
                 # Remplacez 'votre_script.sh' par le chemin vers votre script shell
                 script_path = './docker/' + path + '/init_container.sh'

                 # Liste des arguments à passer au script shell
                 arguments = [args_dict['service_id'], args_dict['service_password']]
 
                 # Utilisation de os.system pour exécuter le script en tant que superutilisateur
                 os.system(f'sudo sh {script_path} {" ".join(arguments)}')
             else:
                 print('Le fichier init du container n existe pas')
    #regarder si les scripts sont lancés automatiquement par crontab

    
    
    #sinon les ajouter avec le script
    
    
        
    #else:
        #return ('Please provide valid ecom_id and ecom_password')

if __name__ == "__main__":
    print(main())
