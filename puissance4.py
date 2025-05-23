import tkinter as tk
import random as rd
from tkinter import colorchooser, messagebox, font
from PIL import Image, ImageTk
import time 

# On initialise juste les variables globales
jeu_actif = False
lignes = 0
colonnes = 0
dim_case = 80
grille = [[None] * colonnes for _ in range(lignes)]
joueurs = [
    {"nom": None, "couleur": None, "Joker": True, "victoires":0},
    {"nom": None, "couleur": None, "Joker": True, "victoires":0}]
liste_coups = []
jetons_pour_gagner = 0
#ça pas touche, c'est juste pour stocker de coté les couleurs 
color_j1 = None
color_j2 = None

#Contenu fenêtre principale/config
root=tk.Tk()
root.title("Menu Puissance 4")

font.nametofont("TkDefaultFont").configure(family="Segoe UI", size=11)
bouton_style_1 = {"bg": "#1ABC9C", "fg": "white", "font": ("Arial", 11, "bold"), "bd": 2, "relief": "groove"}
bouton_style_2 = {"bg": "#C0392B", "fg": "white", "font": ("Arial", 11, "bold"), "bd": 2, "relief": "groove"}
bouton_style_3 = {"bg": "#FFD700", "fg": "white", "font": ("Arial", 11, "bold"), "bd": 2, "relief": "groove"}

frame = tk.Frame(root)
frame.grid(padx=20, pady=20)

espace_gauche = tk.Frame(frame)
espace_gauche.grid(row=0, column=0, padx=10)
image = ImageTk.PhotoImage(Image.open("PIL/GAMEPIC.png").resize((400, 400)))
tk.Label(espace_gauche, image=image).grid()

espace_droite = tk.Frame(frame)
espace_droite.grid(row=0, column=1, padx=10)

grille_frame = tk.LabelFrame(espace_droite, text="Configuration de la Grille", padx=10, pady=10)
grille_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=5)
tk.Label(grille_frame, text="Nombre de lignes :").grid(row=0, column=0, sticky="w")
entree_lignes = tk.Entry(grille_frame)
entree_lignes.grid(row=0, column=1)
entree_lignes.insert(0, "6")
tk.Label(grille_frame, text="Nombre de colonnes :").grid(row=1, column=0, sticky="w")
entree_colonnes = tk.Entry(grille_frame)
entree_colonnes.grid(row=1, column=1)
entree_colonnes.insert(0, "7")
tk.Label(grille_frame, text="Jetons pour gagner :").grid(row=2, column=0, sticky="w")
entree_nb_jetons = tk.Entry(grille_frame)
entree_nb_jetons.grid(row=2, column=1)
entree_nb_jetons.insert(0, "4")


joueurs_frame = tk.LabelFrame(espace_droite, text="Joueurs", padx=10, pady=10)
joueurs_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=5)
tk.Label(joueurs_frame, text="Nom Joueur 1 :").grid(row=0, column=0, sticky="w")
entree_nom_joueur1 = tk.Entry(joueurs_frame)
entree_nom_joueur1.grid(row=0, column=1)
entree_nom_joueur1.insert(0, "Joueur 1")
bouton_color_j1 = tk.Button(joueurs_frame, text="Couleur", bg=color_j1, command=lambda: choisir_couleur(0, bouton_color_j1))
bouton_color_j1.grid(row=0, column=2, padx=5)
tk.Label(joueurs_frame, text="Nom Joueur 2 :").grid(row=1, column=0, sticky="w")
entree_nom_joueur2 = tk.Entry(joueurs_frame)
entree_nom_joueur2.grid(row=1, column=1)
entree_nom_joueur2.insert(0, "Joueur 2")
bouton_color_j2 = tk.Button(joueurs_frame, text="Couleur", bg=color_j2, command=lambda: choisir_couleur(1, bouton_color_j2))
bouton_color_j2.grid(row=1, column=2, padx=5)
tk.Label(joueurs_frame, text="Joker autorisé ?").grid(row=2, column=0, sticky="w")
joker_variable = tk.StringVar(value="Oui")
tk.OptionMenu(joueurs_frame, joker_variable, "Oui", "Non").grid(row=2, column=1, columnspan=2, sticky="w")

boutons_frame = tk.LabelFrame(espace_droite, text="Lancement", padx=10, pady=10)
boutons_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")
tk.Button(boutons_frame, text="Partie rapide", width=15, command=lambda: lancer_jeu("rapid"), **bouton_style_1).grid(row=0, column=0, padx=5, pady=2)
tk.Button(boutons_frame, text="Nouvelle partie", width=15, command=lambda: lancer_jeu(False), **bouton_style_1).grid(row=0, column=1, padx=5, pady=2)
tk.Button(boutons_frame, text="Charger partie", width=15, command=lambda: lancer_jeu(True), **bouton_style_1).grid(row=0, column=2, padx=5, pady=2)

def verif_config():
    if not entree_lignes.get().isdigit() or not entree_colonnes.get().isdigit():
        tk.messagebox.showerror("Attention", "Erreur de dimensions.")
        return False

    lignes = int(entree_lignes.get())
    colonnes = int(entree_colonnes.get())
    if lignes < 4 or lignes > 8 or colonnes < 4 or colonnes > 8:
        tk.messagebox.showerror("Attention", "Les dimensions doivent être comprises  entre 4x4 et 8x8.")
        return False

    if not entree_nb_jetons.get().isdigit():
        tk.messagebox.showerror("Erreur", "Erreur de nombre de jetons")
        return False

    jetons = int(entree_nb_jetons.get())
    if jetons < 3 or jetons > 7:
        tk.messagebox.showerror("Erreur", "Le nombre de jetons pour gagner doit être compris entre 3 et 7.")
        return False

    if not entree_nom_joueur1.get().strip() or not entree_nom_joueur2.get().strip():
        tk.messagebox.showerror("Erreur", "Veuillez renseigner un nom pour chaque joueur !")
        return False

    if not color_j1 or not color_j2:
        tk.messagebox.showerror("Erreur", "Veuillez séléctionner une couleur pour chaque joueur !")
        return False

    return True

def choisir_couleur(index, bouton):
    global color_j1
    global color_j2
    couleur = colorchooser.askcolor(title="Choisir une couleur")[1]
    if couleur:
        if index == 0:
            color_j1 = couleur
        elif index == 1:
            color_j2 = couleur
        bouton.config(bg=couleur)

def matchmaking():
    """fonction qui choisit aléatoirement quel joueur commence"""
    joueur_actuel = rd.choice(joueurs)
    return joueur_actuel

def selection_joueur():
    """fonction qui change le tour du joueur"""
    global joueur_actuel
    if joueur_actuel == joueurs[0]:
        joueur_actuel = joueurs[1]
    else:
        joueur_actuel = joueurs[0] 

def afficher_grille():
    """fonction qui affiche la grille de jeu"""
    canvas.delete("all")
    for i in range(lignes):
        for j in range(colonnes):
            x1= j * dim_case + 5
            y1 = i * dim_case + 5
            x2= x1 + dim_case - 10
            y2 = y1 + dim_case - 10
            if grille[i][j] is None:
                couleur = "white"
            else:
                case = grille[i][j]
                couleur = case["couleur"]
            canvas.create_oval(x1, y1, x2, y2, fill=couleur, outline="black", width=4)

start_time = None  
label_timer = None  

def lancer_timer():
    """Fonction pour démarrer le timer"""
    global start_time, label_timer
    start_time = time.time()

    
    label_timer = tk.Label(frame_boutons, text="Temps écoulé : 00:00", font=("Helvetica", 12, "bold"), fg="white", bg="#2C3E50")
    label_timer.grid(row=0, column=0, padx=10, pady=10)

    def mettre_a_jour_timer():
        if not jeu_actif: 
            return
        if start_time:
            elapsed_time = time.time() - start_time
            minutes = int(elapsed_time // 60)
            secondes = int(elapsed_time % 60)
            label_timer.config(text=f"Temps écoulé : {minutes:02d}:{secondes:02d}")
        
        
        fenetre_jeu.after(1000, mettre_a_jour_timer)
    
    mettre_a_jour_timer()

def interagir_jeu(event):
    """fonction qui permet de placer son jeton dans la grille"""
    global joueur_actuel
    global jeu_actif
    if not jeu_actif:
        return
    else:
        colonne = event.x // dim_case
        for i in range(lignes - 1, -1, -1):
            if grille[i][colonne] is None:
                grille[i][colonne] = joueur_actuel
                liste_coups.append([i, colonne, joueur_actuel])
                afficher_grille()
                if verifier_victoire(i, colonne):
                    fenetre_congrats(joueur_actuel)
                    ajouter_victoire(joueur_actuel)
                    jeu_actif = False
                    return
                elif match_nul():#recommendation de la prof : ajout de la condition pour que si toute la grille est remplie, ca affiche match nul
                    return
                selection_joueur()
                return
    

def verifier_vertical(ligne, colonne, couleur):
    """verifie si un joueur a gagné verticalement"""
    compteur = 0
    for k in range(-jetons_pour_gagner + 1, jetons_pour_gagner):
        if 0 <= (ligne + k) and (ligne + k) < lignes:
            if couleur == grille[ligne+k][colonne]:
                compteur += 1
            else:
                compteur = 0
            if compteur == jetons_pour_gagner:
                return True
        
    return False


def verifier_horizontal(ligne, colonne, couleur):
    """verifie si un joueur a gagné horizontalement"""
    compteur = 0
    for k in range(-jetons_pour_gagner + 1, jetons_pour_gagner):
        if 0 <= (colonne + k) and (colonne + k) < colonnes:
            if couleur == grille[ligne][colonne+k]:
                compteur += 1
            else:
                compteur = 0
            if compteur == jetons_pour_gagner:
                return True
    return False

def verifier_diagonale(ligne, colonne, couleur):
    """verifie si un joueur a gagné en diagonale"""
    compteur = 0
    for k in range(-jetons_pour_gagner + 1, jetons_pour_gagner):
        if (0 <= (colonne + k) and (colonne + k) < colonnes) and (0 <= (ligne + k) and (ligne + k) < len(grille)):
            if couleur == grille[ligne+k][colonne+k]:
                compteur += 1
            else:
                compteur = 0
            if compteur == jetons_pour_gagner:
                return True 
    compteur = 0
    for k in range(-3, 4):
        if (0 <= (colonne + k) and (colonne + k) < colonnes) and (0 <= (ligne - k) and (ligne - k) < len(grille)):
            if couleur == grille[ligne-k][colonne+k]:
                compteur += 1
            else:
                compteur = 0
            if compteur == jetons_pour_gagner:
                return True 
    return False


def verifier_victoire(ligne, colonne):
    """verifie si un joueur a gagné en appelant les 3 fonctions ci-dessus"""
    couleur = joueur_actuel
    if verifier_vertical(ligne, colonne, couleur) or verifier_horizontal(ligne, colonne, couleur) or verifier_diagonale(ligne, colonne, couleur):
        return True
    return False

def utiliser_joker(event):
    """Cette fonction permet de lorsque nous faisons un clic droit annuler le coup de l'autre joueur"""
    global grille, liste_coups, joueurs
    if joueur_actuel["Joker"]:
        grille[liste_coups[-1][0]][liste_coups[-1][1]] = None
        afficher_grille()
        liste_coups.pop(-1)
        if joueurs[0] == joueur_actuel:
            joueurs[0]["Joker"] = False
        else:
            joueurs[1]["Joker"] = False
    else:
        return

def fenetre_congrats(joueur):#ici aussi, on doit restyliser
    """affiche une fenetre de victoire lorsqu'un joueur gagne""" 
    global jeu_actif
    jeu_actif = False
    
    fenetre2 = tk.Toplevel()
    fenetre2.title("Victoire !")
    message_victoire = joueur["nom"] + " a gagné !"
    tk.Label(fenetre2, text=message_victoire, fg=joueur["couleur"], font=("Arial", 11, "bold")).grid(row=0, columnspan=2, pady=20)
    tk.Button(fenetre2, text="Recommencer", command=lambda: recommencer(fenetre2), **bouton_style_1).grid(row=1, column=0, padx=10, pady= 10)
    tk.Button(fenetre2, text="Quitter", command=quitter, **bouton_style_2).grid(row=1, column=1, padx=10, pady=10)  #enft, fallait passer fenetre2 comme argument
    fenetre2.protocol("WM_DELETE_WINDOW", root.destroy)

def ajouter_victoire(joueur):
    joueur["victoires"] += 1

def afficher_scores():
    fenetre_score = tk.Toplevel()
    fenetre_score.title("Scores")
    for idx, joueur in enumerate(joueurs):
        score_txt = f"{joueur["nom"]} : {joueur["victoires"]} victoire(s)"
        tk.Label(fenetre_score, text=score_txt, fg=joueur["couleur"]).grid(row=idx, column=0, pady=5)

def match_nul():#la fonction marche
    """affiche une fenetre de match nul"""
    global jeu_actif
    if all(None not in ligne for ligne in grille):
        jeu_actif = False
        fenetre3 = tk.Toplevel(root)
        fenetre3.title("Match nul !")
        label = tk.Label(fenetre3, text="Match nul ! Personne n'a gagné.", fg="orange", font=("Arial", 11, "bold"))
        label.grid(columnspan=2, row=0, padx=50)
        label2 = tk.Label(fenetre3, text="Sélectionnez une option:", fg="orange", font=("Arial", 11, "bold"))
        label2.grid(columnspan=2, row=1, padx=50)
        bouton_recommencer = tk.Button(fenetre3, text="Recommencer", command=lambda: recommencer(fenetre3), **bouton_style_1)
        bouton_recommencer.grid(column=0, row=2, padx=10, pady=10)
        bouton_fermer = tk.Button(fenetre3, text="Quitter", command=quitter, **bouton_style_2)
        bouton_fermer.grid(column=1, row=2, padx=50)
        fenetre3.protocol("WM_DELETE_WINDOW", root.destroy)
        return True

    return False

def recommencer(fenetre):
    """fonction qui permet de recommencer la partie"""
    global jeu_actif, grille, joueur_actuel
    jeu_actif = True
    grille = [[None] * colonnes for _ in range(lignes)]
    joueur_actuel = matchmaking()
    joueurs[0]["Joker"], joueurs[1]["Joker"] = True, True
    if fenetre!=root:
        fenetre.destroy()
    afficher_grille()
    lancer_timer()

def quitter():
        if messagebox.askyesno("Confirmation", "Veux-tu vraiment quitter ?"):
            root.destroy()


def sauvegarder():
    '''la fonction se charge de sauvegarder la partie en cours'''
    #seul problème c'est que le dossier doit préexister. j'ai crée le dossier savegame sur github
    fichier = open("savegame/savegame.txt", "w")
    couleur_j0=joueurs[0]["couleur"]
    couleur_j1=joueurs[1]["couleur"]

    if joueur_actuel==joueurs[0]:
        fichier.write("0\n")
    else:
        fichier.write("1\n")

    fichier.write(f"{joueurs[0]["nom"]}-{joueurs[0]["couleur"]}\n")
    fichier.write(f"{joueurs[1]["nom"]}-{joueurs[1]["couleur"]}\n")

    fichier.write(f"{jetons_pour_gagner}\n")
    
    fichier.write(f"{joueurs[0]["Joker"]}-{joueurs[1]["Joker"]}\n")

    fichier.write(f"{lignes}x{colonnes}\n")

    for i in grille:
            for j in i:
                if j is None:
                    fichier.write("#")
                elif j["couleur"] == couleur_j0:
                    fichier.write("0")
                elif j["couleur"] == couleur_j1:
                    fichier.write("1")
            fichier.write("\n")
    fichier.close()
    tk.messagebox.showinfo("Sauvegarde de la partie...", "Partie sauvegardée avec succès.")

def charger():

    fichier=open("savegame/savegame.txt", "r")
    li=fichier.readlines()

    joueur_actuel=li[0].strip()

    ligne_joueur_0=li[1].strip().split("-")
    nom_joueur1=ligne_joueur_0[0]
    couleur_joueur1=ligne_joueur_0[1]

    ligne_joueur_1=li[2].strip().split("-")
    nom_joueur2=ligne_joueur_1[0]
    couleur_joueur2=ligne_joueur_1[1]

    nombre_jetons_sv=int(li[3].strip())

    jokers=li[4].strip().split("-")
    joker_1=jokers[0]
    joker_2=jokers[1]

    dimensions=li[5].strip().split("x")
    dimensions_ligne=int(dimensions[0])
    dimensions_colonne=int(dimensions[1])

    joueurs = [
            {"nom": nom_joueur1, "couleur": couleur_joueur1, "Joker": joker_1, "victoires":0},
            {"nom": nom_joueur2, "couleur": couleur_joueur2, "Joker": joker_2, "victoires":0}]
    
    joueur_actuel_sv=joueurs[int(joueur_actuel)]

    grille_sv = [["#" for _ in range(dimensions_colonne)] for _ in range(dimensions_ligne)]
    cpt = 0
    while cpt < dimensions_ligne:
        ligne_save = li[6 + cpt].strip()
        j = 0
        while j < dimensions_colonne:
            if ligne_save[j] == "0":
                grille_sv[cpt][j] = joueurs[0]
            elif ligne_save[j] == "1":
                grille_sv[cpt][j] = joueurs[1]
            elif ligne_save[j] == "#":
                grille_sv[cpt][j] = None
            j += 1
        cpt += 1
    fichier.close()
    tk.messagebox.showinfo("Partie chargée !",f"Le joueur actuel est {joueurs[int(joueur_actuel)]["nom"]}")
    return dimensions_ligne, dimensions_colonne, grille_sv, joueur_actuel_sv, joueurs, nombre_jetons_sv


def lancer_jeu(charger_partie=False):
    global lignes, colonnes, joueur_actuel, joueurs,grille,jeu_actif,canvas,canvas_frame, jetons_pour_gagner, fenetre_jeu, frame_boutons

    if jeu_actif==True:
        tk.messagebox.showwarning("Action imposible","Une partie est déja en cours")
        return

    if charger_partie==True:
        lignes, colonnes, grille,joueur_actuel, joueurs, jetons_pour_gagner = charger()

    elif charger_partie=="rapid":
        lignes=6
        colonnes=7
        grille = [[None] * colonnes for _ in range(lignes)]
        joueurs = [
            {"nom": "Joueur 1", "couleur": "red", "Joker": False, "victoires":0},
            {"nom": "Joueur 2", "couleur": "yellow", "Joker": False, "victoires":0}]
        joueur_actuel = matchmaking()
        jetons_pour_gagner = 4

    elif charger_partie==False:

        if not verif_config():
            return
        
        lignes = int(entree_lignes.get())
        colonnes = int(entree_colonnes.get())
        grille = [[None] * colonnes for _ in range(lignes)]
        joueurs = [
            {"nom": entree_nom_joueur1.get(), "couleur": color_j1, "Joker": True, "victoires":0},
            {"nom": entree_nom_joueur2.get(), "couleur": color_j2, "Joker": True, "victoires":0}]
        if joker_variable.get()=="Non":
            joueurs[0]["Joker"]=False
            joueurs[1]["Joker"]=False
        joueur_actuel = matchmaking()
        jetons_pour_gagner = int(entree_nb_jetons.get())

    root.iconify()
    jeu_actif=True
    fenetre_jeu = tk.Toplevel()
    fenetre_jeu.configure(bg="#2C3E50")
    fenetre_jeu.title("Puissance 4")
    canvas_frame = tk.Frame(fenetre_jeu, bd=7, relief="ridge")
    canvas_frame.grid(row=0, column=1)
    canvas = tk.Canvas(canvas_frame, width=colonnes * dim_case, height=lignes * dim_case, bg="#2C3E50")
    canvas.grid()
    canvas.bind("<Button-1>", interagir_jeu)
    canvas.bind("<Button-3>", utiliser_joker)
    afficher_grille()
    
    frame_boutons = tk.Frame(fenetre_jeu, bg="#2C3E50")
    frame_boutons.grid(row=0, column=0)

    bouton_scores = tk.Button(frame_boutons, text="Voir les scores", command=afficher_scores, **bouton_style_3)
    bouton_scores.grid(row=1, pady=5)
    bouton_sauvegarde = tk.Button(frame_boutons, text="Sauvegarder", command=sauvegarder, **bouton_style_1)
    bouton_sauvegarde.grid(row=5, pady=5)
    bouton_quitter = tk.Button(frame_boutons, text="Quitter", command=quitter, **bouton_style_2)
    bouton_quitter.grid(row=6, pady=5)

    fenetre_jeu.protocol("WM_DELETE_WINDOW", root.destroy)
    lancer_timer()
root.mainloop()
