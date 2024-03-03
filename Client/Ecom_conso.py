import re
import tkinter as tk
from datetime import datetime, timedelta
from tkinter import messagebox
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Importations des modules personnalisés
from sae503_MQTT import *
from sae503_NASA import *
from sae503_Meross import *
from sae503_shelly import *
from sae503_bdd_get import *
from sae503_OpenWeather import *
from sae_601_emylo_google import*
from sae_601_oauth2 import get_token, get_user_groups, get_user_list
            
Ville=execute_stored_procedure('GET_maison')

nasameteo={}

for ville in Ville:
    nasameteo[str(ville[0])]={}
    #Récupération de la météo du jour avec OpenWeather
    result=get_city_data(ville[1],"e5906fc1e4373743e5427b4675940341")
    city_data=extract_city_data(result)
    coords,meteo,meteo_data=extract_city_data(result)
    nasameteo[str(ville[0])]["coords"]=coords
    nasameteo[str(ville[0])]['meteo']=meteo
    nasameteo[str(ville[0])]['meteo_data']=meteo_data
    nasameteo[str(ville[0])]['ville']=str(ville[1])
    

    #Connexion à l'API de la NASA
    api_key = " MT3OO5rAXdt2JNwI75yCNc20mwIhuIkXtPqpUreI"

    url = "https://power.larc.nasa.gov/api/temporal/hourly/point"

    lat = coords["lat"]  
    long = coords["lon"]

    #Ajustement du format de la date #start_date = "20220101"
    start_date=datetime.now()-timedelta(days=366)
    start_date_f = start_date.strftime("%Y%m%d")
    start_date_f=start_date_f.replace('-','')

    #Ajustement du format de la date #end_date = "20220102"
    end_date=datetime.now()-timedelta(days=365)
    end_date_f = end_date.strftime("%Y%m%d")
    end_date_f=end_date_f.replace('-','')

    #Récupération de l'ensoleillement avec l'API de la Nasa
    datanasa=("NASA : ",get_NASA_data(url,lat,long,start_date_f,end_date_f,api_key))
    nasameteo[str(ville[0])]['datanasa']=datanasa

    
    
#Création de l'interface graphique
class InterfaceGraphique(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ECOM_conso")
        self.geometry("1300x800")
        self.username = None  # Ajout d'un attribut pour stocker le nom d'utilisateur
        self.user_label = None  # Ajout d'un attribut pour le Label du nom d'utilisateur
        self.afficher_page_connexion()
        self.menu_stack = []
        self.groups = None
        self.group_names = None
        self.current_group_name = None
        
    def handle_logout(self):
    # Optionnel : Ajoutez ici tout traitement nécessaire à la déconnexion.
    # Par exemple, nettoyer des données utilisateur, fermer des connexions réseau, etc.

    # Retournez à la page de connexion
        self.afficher_page_connexion()

    def afficher_page_connexion(self):
        self.configure(bg='#092433')
        for widget in self.winfo_children():
            widget.destroy()

        # Configurez les colonnes et les rangées pour centrer les widgets
        self.grid_columnconfigure(0, weight=1)
        # Ajoutez des configurations de ligne pour l'espace au-dessus et en dessous des widgets de connexion
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(6, weight=2)  # Si vous avez 5 rangées de widgets de connexion

        # Chargement et affichage du logo ECOM
        logo_path = r"Logo\logo_texte.png"
        logo_image = Image.open(logo_path)
        logo_image = logo_image.resize((640, 400), Image.LANCZOS)
        tk_logo_image = ImageTk.PhotoImage(logo_image)

        # Ajout du logo en utilisant grid
        logo_label = tk.Label(self, image=tk_logo_image, bg='#092433')
        logo_label.image = tk_logo_image  # Gardez une référence à l'image
        logo_label.grid(row=0, column=0)  # Positionnez le logo

        # Nom d'utilisateur
        username_label = tk.Label(self, text="Nom d'utilisateur:", bg='#092433', fg='white')
        username_label.grid(row=1, column=0, sticky="ew")
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=2, column=0, sticky="ew", padx=600)

        # Mot de passe
        password_label = tk.Label(self, text="Mot de passe:", bg='#092433', fg='white')
        password_label.grid(row=3, column=0, sticky="ew")
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=4, column=0, sticky="ew", padx=600)

        # Bouton de connexion
        connexion_button = tk.Button(self, text="Connexion", command=self.gerer_connexion)
        connexion_button.grid(row=5, column=0, sticky="ew", padx=600, pady=5)

        # Assurez-vous que les widgets ne s'étendent pas plus que nécessaire
        for i in range(1, 6):
            self.grid_rowconfigure(i, weight=0)

    def gerer_connexion(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        token_info = get_token('192.168.1.105', '8080', username, password)
        group_names = []

        if 'access_token' in token_info:
            self.token = token_info['access_token']
            self.username = username  # Stockage du nom d'utilisateur
            token_script=get_token('192.168.1.105', '8080', 'script', 'admin')
            user=get_user_list('192.168.1.105', '8080', token_script['access_token'])
            try:
                trouvé=False
                for dic in user:
                    if (dic['username'] == username):
                        ecom=get_user_groups('192.168.1.105','8080',token_script['access_token'],dic["id"])
                        for i in ecom:
                            if i['name']=='Ecom':
                                trouvé=True
                                group_names = [group['name'] for group in ecom]
                                self.initialiser_interface(group_names)
                        if not trouvé:      
                            messagebox.showerror("Erreur de connexion", "Nom d'utilisateur ou mot de passe incorrect ou accès non autorisé") 
            except Exception as e:
                print(e)
                messagebox.showerror("Erreur de connexion", "Nom d'utilisateur ou mot de passe incorrect ou accès non autorisé")
        else:
            messagebox.showerror("Erreur de connexion", "Nom d'utilisateur ou mot de passe incorrect ou accès non autorisé")

    def afficher_nom_utilisateur(self):
            # Si un Label pour le nom d'utilisateur existe déjà, le mettre à jour.
            # Sinon, créez un nouveau Label.
            if self.user_label is not None and self.user_label.winfo_exists():
                self.user_label.config(text=f"Utilisateur : {self.username}")
            else:
                self.user_label = tk.Label(self, text=f"Utilisateur : {self.username}", bg='#092433', fg='white', font=("Helvetica", 10))
                # Vous devrez choisir un gestionnaire de géométrie ici, `pack`, `grid`, ou `place`.
                self.user_label.pack(side="bottom", anchor="e", padx=10, pady=10)
    
    def get_data_maison(self, liste_maison):
        d_maison={}
        for Maison in liste_maison:
            d={}
            if not Maison == 'Ecom':
                id_maison = Maison.replace('Maison ', "")
                plug_list_unsorted =execute_stored_procedure("GET_objets",int(id_maison))
                plug_list_with_false=sorted(plug_list_unsorted)
                plug_list = [item for item in plug_list_with_false if item[1] != 'false' and not item[0].startswith('eui')] 
                for P in plug_list:
                    mesures_prises_tuple=execute_stored_procedure("GET_objet_mesures",P[0])
                    print(P)
                    d[P[0]]=mesures_prises_tuple
                    print (mesures_prises_tuple)
                
                #Récupération de la consommation et production par maison
                conso_maison=execute_stored_procedure("GET_conso_maison",int(id_maison))

                #Préparation des dictionnaires pour la production, consommation et différence des deux
                heure_prod={}
                heure_conso={}
                heure_diff={}
                try:
                    for conso in conso_maison:
                        #Récupération de la production par heure
                        heure_prod[conso[2]]=conso[1]
                        #Récupération de la consommation par heure
                        heure_conso[conso[2]]=conso[0]
                        #Récupération de la différence production/consommation par heure
                        heure_diff[conso[2]]=conso[3]
                    d["heure_prod"]=heure_prod
                    d["heure_conso"]=heure_conso
                    d["heure_diff"]=heure_diff
                    d_maison[Maison]=d
                except Exception as e:
                    print(e)
                    d_maison[Maison]=d
        return d_maison
                    
    def initialiser_interface(self, groups):
        # Nettoyer l'interface et reconstruire l'interface utilisateur principale
        for widget in self.winfo_children():
            widget.destroy()

        # Ici, vous devriez reconstruire votre interface utilisateur principale
        # comme avant, mais après une authentification réussie.
        # Par exemple:
        self.groups = groups  # Stockez les groupes dans l'attribut self.groups
        self.create_main_menu(groups)
        self.configure(bg='#092433')
        self.afficher_nom_utilisateur()
        
        self.data = self.get_data_maison(groups)

    def set_window_icon(self):
            # Chemin vers le fichier ICO (format d'icône)
            chemin_icon = r"Logo\logo.ico"
            # Définition de l'icône avec la méthode iconbitmap()
            self.iconbitmap(chemin_icon)

    #Création du menu principal
    def create_main_menu(self, groups):
        if groups is None:
            groups = self.groups
        # Supprimez tous les widgets existants
        for widget in self.winfo_children():
            widget.destroy()
        
        self.current_state = 'main_menu'

        # Configurez les colonnes et les rangées pour centrer les boutons
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=100)
        

        # Chargement du logo ECOM
        logo_path = r"Logo\logo_texte.png"
        logo_image = Image.open(logo_path)
        logo_image = logo_image.resize((320, 200), Image.LANCZOS)
        tk_logo_image = ImageTk.PhotoImage(logo_image)

        # Ajout du logo en utilisant grid
        logo_label = tk.Label(self, image=tk_logo_image)
        logo_label.image = tk_logo_image  # Gardez une référence à l'image
        logo_label.grid(row=0, column=0)  # Positionnez le logo

        # Cadre pour centrer les boutons des maisons
        center_frame = tk.Frame(self, bg="#092433")
        center_frame.grid(row=1, column=0, sticky="ew")

        # Ajoutez une configuration de colonne au cadre central pour centrer les boutons
        center_frame.grid_columnconfigure(0, weight=1)

        # Ajoutez les boutons des maisons au cadre central
        for i, group in enumerate(groups):
            if group != 'Ecom':  # Filtrez le groupe 'Ecom'
                button_text = f"{group}"
                button = tk.Button(
                    center_frame,
                    text=button_text,
                    command=lambda group_name=group: self.show_sub_menu(group_name),
                    font=("Helvetica", 14),
                    bg="#e77b0d",
                    fg="white",
                    padx=20,
                    pady=10,
                )
                # Positionnez chaque bouton dans le cadre central en utilisant grid
                button.grid(row=i, column=0, pady=20, padx=500, sticky="ew")
                
        
    # Création d'un cadre pour le label utilisateur et le bouton de déconnexion
        user_frame = tk.Frame(self, bg='#092433')
        user_frame.grid(row=2, column=0, sticky="se", padx=10, pady=10)

        self.user_label = tk.Label(user_frame, text=f"Utilisateur : {self.username}", bg='#092433', fg='white', font=("Helvetica", 10))
        self.user_label.pack(side="right", padx=5, pady=10)

        # Ajout du bouton de déconnexion dans le cadre
        logout_button = tk.Button(
            user_frame,
            text="Déconnexion",
            command=self.handle_logout,
            font=("Helvetica", 12),
            bg="lightblue",
            fg="black",
            padx=10,
            pady=5
        )
        logout_button.pack(side="left", padx=5, pady=10)

                
    #Définition des menus maisons
    def show_sub_menu(self, group_name):
        # Supprime tous les widgets existants
        self.destroy_widgets()
        self.current_group_name = group_name
        self.menu_stack.append(self.current_state)
        self.current_state = 'sub_menu'

        spacer_top = tk.Frame(self, height=10, bg="#092433")
        spacer_top.pack(side="top", fill="x")

        # Ajout d'un bouton pour revenir au menu principal
        back_button = tk.Button(
            self,
            text="Retour au Menu Principal",
            command=lambda: self.create_main_menu(self.groups), 
            font=("Helvetica", 12),
            bg="lightcoral",
            fg="black",
            padx=20,
            pady=5,
        )
        back_button.pack(pady=(5, 2), padx=20)

        # Ajout d'un bouton pour accéder au menu appareils
        devices_button = tk.Button(
            self,
            text="Accueil Appareils",
            command=lambda: self.show_device_menu(group_name),
            font=("Helvetica", 12),
            bg="lightgreen",
            fg="black",
            padx=20,
            pady=5,
        )
        devices_button.pack(pady=(2, 20), padx=20)

        id_maison = str(group_name.replace('Maison ', ""))
        
        # Chargez les images des icônes météo
        base_path = r"image_meteo\\"
        image_codes = ["01d", "01n", "02d", "02n", "03d", "03n", "04d", "04n", "09d", "09n", "10d", "10n", "11d", "11n", "13d", "13n", "50d", "50n"]
        image_paths = {code: f"{base_path}{code}.png" for code in image_codes}
        weather_icon = Image.open(image_paths[nasameteo[str(id_maison)]['meteo']["icon"]])
        weather_icon = weather_icon.resize((170, 170), Image.LANCZOS)
        tk_weather_icon = ImageTk.PhotoImage(weather_icon)

        # Création d'un cadre pour contenir l'image et le label
        info_frame = tk.Frame(self, bg='#092433')
        info_frame.pack(pady=(5, 10))

        # Création de l'étiquette pour l'icône météo
        icon_label = tk.Label(info_frame, image=tk_weather_icon, bg='#092433')
        icon_label.image = tk_weather_icon
        icon_label.pack(side="left")
        
        # Ajout de l'étiquette pour la température et autres informations météo
        if meteo_data['temp'] < 10:
            temp_label = tk.Label(info_frame, text=f"Température à {nasameteo[str(id_maison)]['ville']}: {nasameteo[str(id_maison)]['meteo_data']['temp']}°C", bg="#092433", fg="lightblue", font=("Helvetica", 18))
            temp_label.pack(side="left", padx=10)  # Ajout d'un espace entre l'icône et le texte avec padx
        elif meteo_data['temp'] >10 and meteo_data['temp'] <20:
            temp_label = tk.Label(info_frame, text=f"Température à {nasameteo[str(id_maison)]['ville']}: {nasameteo[str(id_maison)]['meteo_data']['temp']}°C", bg="#092433", fg="yellow", font=("Helvetica", 18))
            temp_label.pack(side="left", padx=10)  # Ajout d'un espace entre l'icône et le texte avec padx
        elif meteo_data['temp'] >20 and meteo_data['temp'] <30:
            temp_label = tk.Label(info_frame, text=f"Température à {nasameteo[str(id_maison)]['ville']}: {nasameteo[str(id_maison)]['meteo_data']['temp']}°C", bg="#092433", fg="#e7760d", font=("Helvetica", 18))
            temp_label.pack(side="left", padx=10)  # Ajout d'un espace entre l'icône et le texte avec padx
        else:
            temp_label = tk.Label(info_frame, text=f"Température à {nasameteo[str(id_maison)]['ville']}: {nasameteo[str(id_maison)]['meteo_data']['temp']}°C", bg="#092433", fg="red", font=("Helvetica", 18))
            temp_label.pack(side="left", padx=10)  # Ajout d'un espace entre l'icône et le texte avec padx
        # Mettez à jour ou créez le label utilisateur si ce n'est pas déjà fait
        if self.user_label and self.user_label.winfo_exists():
            self.user_label.config(text=f"Utilisateur : {self.username}")
        else:
            self.user_label = tk.Label(self, text=f"Utilisateur : {self.username}", bg='#092433', fg='white', font=("Helvetica", 10))
            self.user_label.pack(side="bottom", anchor="se")

        # Création de l'espace pour les graphiques
        # Création de deux sous-cadres dans graph_frame
        
        graph_frame = tk.Frame(self, bg="#092433")
        graph_frame.pack(fill="both", expand=True)
        top_frame = tk.Frame(graph_frame, bg="#092433")
        bottom_frame = tk.Frame(graph_frame, bg="#092433")
        
        top_frame.pack(side="top", pady=5)
        bottom_frame.pack(side="bottom", pady=5)

        # Extraction des données de l'API de la Nasa
        nasa_data = datanasa[1]
        nasa_data2=datanasa[1]

        today = datetime.now()-timedelta(days=365)
        # Format the date as per your requirement
        formatted_date = today.strftime("%Y/%m/%d")
        
        for date in list(nasa_data2.keys()):
            if not date.startswith(formatted_date):
                nasa_data.pop(date)
                
        # Création d'une liste avec la date et l'ensoleillement
        dates = list(nasa_data.keys())
        print(dates)
        ensoleillement = list(nasa_data.values())
        
        # Conversion du format de la date pour l'utiliser dans le graphique
        dates = [date.split("-")[1] for date in dates]

        # Ajustement de la taille des légendes
        fig, ax = plt.subplots(figsize=(4, 2))

        # Affichage du graphique et des légendes
        ax.bar(dates, ensoleillement, color='blue', width=0.8)
        ax.set_xlabel('Date et Heure, format: m-d H')
        ax.set_ylabel('Ensoleillement W/m²')
        ax.set_title('NASA Ensoleillement Data')
        ax.tick_params(axis='x', labelsize=7)  # Ajustement de la taille des légendes

        # Format du l'axe des abscisses
        ax.set_yticks([0, 100, 200, 300, 400, 500])  # Positions des graduations
        ax.set_yticklabels(['0', '100', '200', '300', '400', '500'])
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        # Intégration du graphique dans l'interface
        canvas = FigureCanvasTkAgg(fig, master=top_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.config(width=500, height=200)  
        canvas_widget.pack(side="left", padx=10, pady=5)
        
        # Création d'une figure pour le 2eme graphique
        fig2, ax2 = plt.subplots(figsize=(4, 2))
        
        # Création d'une liste avec l'heure et la production
        H_prod = self.data[group_name]['heure_prod'].keys()
        V_prod = self.data[group_name]['heure_prod'].values()
        
        ax2.plot(H_prod, V_prod, color='green', marker='o', linestyle='--')
        
        # Intégration du graphique dans l'interface
        canvas2 = FigureCanvasTkAgg(fig2, master=top_frame)
        canvas_widget2 = canvas2.get_tk_widget()
        canvas_widget2.config(width=500, height=200) 
        canvas_widget2.pack(side="left", padx=10, pady=5)

        
        # Affichage des légendes
        ax2.set_xlabel('Heure')
        ax2.set_ylabel('Production en W')
        ax2.set_title('Production du jour')
        ax2.tick_params(axis='x', labelsize=7)  # Ajustement de la taille des légendes

        #Format de la légende des abscisses
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        # Création d'une figure pour le 3eme graphique
        fig3, ax3 = plt.subplots(figsize=(4, 2))
        
        # Création d'une liste avec l'heure et la production
        H_conso = self.data[group_name]['heure_conso'].keys()
        V_conso = self.data[group_name]['heure_conso'].values()
        
        
        ax3.plot(H_conso, V_conso, color='red', marker='o', linestyle='--')
        
        # Intégration du graphique 3 dans l'interface
        canvas3 = FigureCanvasTkAgg(fig3, master=bottom_frame)
        canvas_widget3 = canvas3.get_tk_widget()
        canvas_widget3.config(width=500, height=400)
        canvas_widget3.pack(side="left", padx=10)

                
        ax3.set_xlabel('Heure')
        ax3.set_ylabel('Consommation en W')
        ax3.set_title('Consommation du jour')
        ax3.tick_params(axis='x', labelsize=7)  # Ajustement de la taille des légendes

        #Format de la légende des abscisses
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        # Création d'une figure pour le 4eme graphique
        fig4, ax4 = plt.subplots(figsize=(4, 2))
        
        # Création d'une liste avec l'heure et la production
        H_diff = self.data[group_name]['heure_diff'].keys()
        V_diff = self.data[group_name]['heure_diff'].values()
        
        ax4.bar(H_diff, V_diff, color='orange', width=1)
        
        # Intégration du graphique 4 dans l'interface
        canvas4 = FigureCanvasTkAgg(fig4, master=bottom_frame)
        canvas_widget4 = canvas4.get_tk_widget()
        canvas_widget4.config(width=500, height=400)
        canvas_widget4.pack(side="left", padx=10)
            
        ax4.set_xlabel('Heure')
        ax4.set_ylabel('Différence Conso/Prod en W')
        ax4.set_title('Différence consommation/production du jour')
        ax4.tick_params(axis='x', labelsize=7)  # Ajustement de la taille des légendes

        # Format des légendes de l'axe des abscisses
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()


        
    def show_device_menu(self, group_name):
        # Supprime tous les widgets existants
        self.destroy_widgets()
        self.current_group_name = group_name
        # Configurez la fenêtre principale pour utiliser pack avec un remplissage vers le haut
        self.pack_propagate(0)  # Empêche le redimensionnement automatique

        # Ajoute un bouton pour revenir au menu précédent
        back_button = tk.Button(
            self,
            text="Retour au Menu Précédent",
            command=self.return_to_previous_menu,
            font=("Helvetica", 12),
            bg="lightcoral",
            fg="black",
            padx=10,
            pady=5,
        )
        back_button.grid(row=0, column=0, pady=10, padx=520, sticky="ew")

        # Ajoute le menu actuel à la pile
        self.menu_stack.append(self.current_state)
        # Met à jour la variable d'état
        self.current_state = "device_menu"

        # Création d'un canevas pour le défilement
        canvas = tk.Canvas(self, bg="#092433")
        canvas.grid(row=1, column=0, sticky="nsew")
        
        # Création d'un cadre pour les boutons dans le canevas
        frame_buttons = tk.Frame(canvas, bg="#092433")
        canvas.create_window((0, 0), window=frame_buttons, anchor="nw")
        
        frame_buttons.grid_columnconfigure(0, weight=1)
        

        # Parcours de chaque maison dans self.data
        dispositifs = self.data.get(group_name, {})
        prises = [nom for nom in dispositifs if not nom.startswith('heure')]

            # Ajouter les boutons pour chaque dispositif (prise)
        for i, prise in enumerate(prises):
            device_button = tk.Button(
                frame_buttons,  # Assurez-vous que ce bouton est ajouté à la bonne frame ou canvas
                text=prise,
                command=lambda prise=prise: self.show_device_submenu(prise),  # Ajustez selon la fonction à appeler
                font=("Helvetica", 12),
                bg="lightgray",
                fg="black",
                padx=10,
                pady=5,
            )
            device_button.grid(row=i+1, column=0, pady=10, sticky="ew")

        # Ajoute le menu actuel à la pile
        self.menu_stack.append("sub_menu")
        # Met à jour le menu actuel
        self.current_menu = "device_menu"

        # Configure le défilement du canevas
        scrollbar = tk.Scrollbar(self, command=canvas.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Configure le canevas pour réagir au redimensionnement
        frame_buttons.bind("<Configure>", lambda event, canvas=canvas: self.on_canvas_configure(event, canvas))

        # Placez le label de l'utilisateur en utilisant pack pour qu'il soit en bas à droite
        # Assurez-vous de pack le label après tous les autres widgets pour qu'il soit en bas
        if self.user_label is not None:
            self.user_label.pack_forget()  # Enlever le label de sa position actuelle
        self.user_label = tk.Label(self, text=f"Utilisateur : {self.username}", bg='#092433', fg='white', font=("Helvetica", 10))
        self.user_label.pack(side="bottom", anchor="e", padx=10, pady=10)


    def show_device_submenu(self, button_number):
        # Supprime tous les widgets existants
        self.destroy_widgets()
        self.afficher_nom_utilisateur()
        
        if not 'eMylo' in button_number:
            mesures = self.data[self.current_group_name][button_number]
            # Exemple d'affichage de mesures pour la prise
            values_W=[]
            for i in self.data[self.current_group_name][button_number]:
                if i[4]== 'W': values_W.append (i[2:5])
            
            Heures=[heure[0].strftime("%H:%M") for heure in values_W]
            Watts=[float(watt[-2]) for watt in values_W]

            
        back_button = tk.Button(
            self,
            text="Retour au Menu Précédent",
            command=self.return_to_previous_menu,
            font=("Helvetica", 12),
            bg="lightcoral",
            fg="black",
            padx=10,
            pady=5,
        )
        back_button.pack(pady=10)
        
        # Ajout du menu actuel à la pile
        self.menu_stack.append(self.current_state)
        # Met à jour la variable d'état
        self.current_state = f"device_submenu_{button_number}"

        # Ajout du contenu spécifique au menu appareil ici
        tk.Label(self, text=f"Menu {button_number}", bg="lightblue").pack()

        # Utilisation d'une expression régulière pour extraire le numéro du menu
        match = re.match(r'^Prise(?:_shelly)?(\d+)$', button_number)
        if "esp" in button_number:
            on_button = tk.Button(
                self,
                text="On",
                command=lambda name=button_number: mqtt_publish(cli,"status/192.168.1.111", "on"),
                font=("Helvetica", 12),
                bg="lightgreen",
                fg="black",
                padx=10,
                pady=5,
            )
            off_button = tk.Button(
                self,
                text="Off",
                command=lambda name=button_number: mqtt_publish(cli,"status/192.168.1.111", "off"),
                font=("Helvetica", 12),
                bg="lightcoral",
                fg="black",
                padx=10,
                pady=5,
            )
            
        elif "eMylo" in button_number:
            on_button = tk.Button(
                self,
                text="On",
                command=lambda: turn_on(button_number, 'your_device_model_id'),
                font=("Helvetica", 12),
                bg="lightgreen",
                fg="black",
                padx=10,
                pady=5,
            )
            off_button = tk.Button(
                self,
                text="Off",
                command=lambda: turn_off(button_number, 'your_device_model_id'),
                font=("Helvetica", 12),
                bg="lightcoral",
                fg="black",
                padx=10,
                pady=5,
            )
        if match:
            menu_number = int(match.group(1))
            if "Prise_shelly" in button_number:
                #Gestion du menu pour une prise Shelly
                shelly_ip = f"192.168.1.128"
                switch_id = f"{menu_number}"
                #Création d'un bouton On et off pour piloter la prise avec la commande change_switch_state du script sae503_Shelly.py
                
                on_button = tk.Button(
                    self,
                    text="On",
                    command=lambda: (
                        change_switch_state(shelly_ip, int(switch_id), True),
                        get_switch_state(shelly_ip,int(switch_id))
                    ),
                    font=("Helvetica", 12),
                    bg="lightgreen",
                    fg="black",
                    padx=10,
                    pady=5,
                )
                off_button = tk.Button(
                    self,
                    text="Off",
                    command=lambda: (
                        change_switch_state(shelly_ip, int(switch_id), False),
                        get_switch_state(shelly_ip,int(switch_id))
                    ),
                    font=("Helvetica", 12),
                    bg="lightcoral",
                    fg="black",
                    padx=10,
                    pady=5,
                )
                
                #Gestion du cas d'une prise Meross
                #Création d'un bouton On et off pour piloter la prise Meross avec la commande exec_meross du script sae503_Meross.py
            elif "Prise" in button_number:
                on_button = tk.Button(
                    self,
                    text="On",
                    command=lambda name=button_number: exec_meross(name, "on"),
                    font=("Helvetica", 12),
                    bg="lightgreen",
                    fg="black",
                    padx=10,
                    pady=5,
                )
                off_button = tk.Button(
                    self,
                    text="Off",
                    command=lambda name=button_number: exec_meross(name, "off"),
                    font=("Helvetica", 12),
                    bg="lightcoral",
                    fg="black",
                    padx=10,
                    pady=5,
                )
                # Gestion du cas d'un esp avec sae503_MQTT.py
            else:
                # Gestion d'autres cas si nécessaire
                on_button = tk.Button(
                    self,
                    text="On",
                    command=lambda: print(f"Commande On par défaut pour Prise{menu_number}"),
                    font=("Helvetica", 12),
                    bg="lightgreen",
                    fg="black",
                    padx=10,
                    pady=5,
                )
                off_button = tk.Button(
                    self,
                    text="Off",
                    command=lambda: print(f"Commande Off par défaut pour Prise{menu_number}"),
                    font=("Helvetica", 12),
                    bg="lightcoral",
                    fg="black",
                    padx=10,
                    pady=5,
                )
        """else:
            # Gestion d'autres cas si nécessaire
            on_button = tk.Button(
                self,
                text="On",
                command=lambda: print("Commande On par défaut"),
                font=("Helvetica", 12),
                bg="lightgreen",
                fg="black",
                padx=10,
                pady=5,
            )
            off_button = tk.Button(
                self,
                text="Off",
                command=lambda: print("Commande Off par défaut"),
                font=("Helvetica", 12),
                bg="lightcoral",
                fg="black",
                padx=10,
                pady=5,
            )
"""
        on_button.pack(pady=5)
        off_button.pack(pady=5)
        
        graph_frame = tk.Frame(self, bg="#092433")
        graph_frame.pack(fill="both", expand=True)
            
        if not 'eMylo' in button_number:   
            # Création d'une figure pour le 2eme graphique
            fig1, ax1 = plt.subplots(figsize=(4, 2))

            
            ax1.plot(Heures, Watts, color='red', marker='o', linestyle='--')
            
            # Intégration du graphique dans l'interface
            canvas1 = FigureCanvasTkAgg(fig1, master=graph_frame)
            canvas_widget1 = canvas1.get_tk_widget()
            canvas_widget1.config(width=500, height=200) 
            canvas_widget1.place(relx=0.5, rely=0.5, anchor="center")

            
            # Affichage des légendes
            ax1.set_xlabel('Heure')
            ax1.set_ylabel('Consommation W')
            ax1.set_title('Consommation du jour')
            ax1.tick_params(axis='x', labelsize=7)
            ax1.set_yticks([0, 20, 40, 60, 80, 100])  # Positions des graduations
            ax1.set_yticklabels(['0', '20', '40', '60', '80', '100'])

            #Format de la légende des abscisses
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
        else:
            self.eMylo_label=tk.Label(master=graph_frame, text= f"La consommation des prises de types eMylo n'est pas prise en charge par Ecom_conso", bg='#092433', fg='#e7760d', font=("Helvetica", 20))
            self.eMylo_label.place(relx=0.5, rely=0.5, anchor="center")

    def return_to_previous_menu(self):
        if self.menu_stack:
            previous_state = self.menu_stack.pop()  # Récupérer le dernier état
            # Utiliser un switch ou une série de if pour déterminer l'action en fonction de previous_state
            if previous_state == 'main_menu':
                self.show_main_menu()
            if previous_state == 'sub_menu':
                    self.show_sub_menu(self.current_group_name)
            if previous_state == 'device_menu':
                self.show_device_menu(self.current_group_name)
        else:
            # Si la pile est vide, retourner au menu principal par défaut
            self.show_main_menu()
            
    def destroy_widgets(self):
        # Détruit tous les widgets actuels dans le canevas
        for widget in self.winfo_children():
            if widget != self.user_label:
                widget.destroy()

    def on_canvas_configure(self, event, canvas):
        # Ajustement de la région de défilement du canevas lorsque celui-ci est redimensionné
        canvas.configure(scrollregion=canvas.bbox("all"))

#Code principal qui gère le lancement de l'application
if __name__ == "__main__":
    app = InterfaceGraphique()
    app.set_window_icon() 
    app.mainloop()