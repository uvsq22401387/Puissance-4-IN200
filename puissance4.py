import tkinter as tk
import random as rd
from tkinter import colorchooser
from tkinter import messagebox
import tkinter.font as tkFont
from PIL import Image, ImageTk

# Variables globales
jeu_actif = True
lignes = 6
colonnes = 7
dim_case = 80
grille = [[None] * colonnes for _ in range(lignes)]
joueurs = [
    {"nom": "Joueur 1", "couleur": "red", "Joker": True},
    {"nom": "Joueur 2", "couleur": "yellow", "Joker": True}]
liste_coups = []

#Contenu fenêtre principale/config
root=tk.Tk()
root.title("Menu Puissance 4")

frame=tk.Frame(root)
frame.grid(padx=20, pady=20)
espace_gauche=tk.Frame(frame)
espace_gauche.grid(row=0, column=0, padx=10)
image=ImageTk.PhotoImage(Image.open("PIL/GAMEPIC.png").resize((200, 200)))
lab_im = tk.Label(espace_gauche, image=image)
lab_im_im=lab_im
lab_im_im.grid()

espace_droite=tk.Frame(frame)
espace_droite.grid(row=0, column=1, padx=10)
tk.Label(espace_droite, text="Nombre de lignes :").grid(row=0, column=0, sticky="w")
entree_lignes = tk.Entry(espace_droite)
entree_lignes.insert(0, "6")
entree_lignes.grid(row=0, column=1)
tk.Label(espace_droite, text="Nombre de colonnes :").grid(row=1, column=0, sticky="w")
entree_colonnes = tk.Entry(espace_droite)
entree_colonnes.insert(0, "7")
entree_colonnes.grid(row=1, column=1)

tk.Label(espace_droite, text="Nom du Joueur 1 :").grid(row=2, column=0, sticky="w")
entree_nom_joueur1 = tk.Entry(espace_droite)
entree_nom_joueur1.insert(0, joueurs[0]["nom"])
entree_nom_joueur1.grid(row=2, column=1)
tk.Label(espace_droite, text="Nom du Joueur 2 :").grid(row=3, column=0, sticky="w")
entree_nom_joueur2 = tk.Entry(espace_droite)
entree_nom_joueur2.insert(0, joueurs[1]["nom"])
entree_nom_joueur2.grid(row=3, column=1)

bouton_color_j1 = tk.Button(espace_droite, text="Couleur Joueur 1", bg=joueurs[0]["couleur"], command=lambda: choisir_couleur(0, bouton_color_j1))
bouton_color_j1.grid(row=4, column=0, sticky="w")
bouton_color_j2 = tk.Button(espace_droite, text="Couleur Joueur 2", bg=joueurs[1]["couleur"], command=lambda: choisir_couleur(1, bouton_color_j2))
bouton_color_j2.grid(row=5, column=0, sticky="w")

frame_boutons = tk.Frame(espace_droite)
frame_boutons.grid(pady=10)
tk.Button(frame_boutons, text="Nouvelle Partie", command=lambda: lancer_jeu(charger_partie=False)).grid(row=0, column=0, padx=5)
tk.Button(frame_boutons, text="Charger Partie", command=lambda: lancer_jeu(charger_partie=True)).grid(row=0, column=1, padx=5)

def choisir_couleur(joueur_index, bouton):
    couleur = colorchooser.askcolor(title="Choisir une couleur")[1]
    if couleur:
        joueurs[joueur_index]["couleur"] = couleur
        bouton.config(bg=couleur)

def matchmaking():
    """fonction qui choisit aléatoirement quel joueur commence"""
    joueur_actuel = rd.choice(joueurs)
    return joueur_actuel
    
joueur_actuel = matchmaking() #cette variable permet de savoir quel joueur doit jouer

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
                    jeu_actif = False
                    return
                elif match_nul():#recommendation de la prof : ajout de la condition pour que si toute la grille est remplie, ca affiche match nul
                    return
                selection_joueur()
                return
    

def verifier_vertical(ligne, colonne, couleur):
    """verifie si un joueur a gagné verticalement"""
    compteur = 0
    for k in range(-3, 4):
        if 0 <= (ligne + k) and (ligne + k) < lignes:
            if couleur == grille[ligne+k][colonne]:
                compteur += 1
            else:
                compteur = 0
            if compteur == 4:
                return True
        
    return False


def verifier_horizontal(ligne, colonne, couleur):
    """verifie si un joueur a gagné horizontalement"""
    compteur = 0
    for k in range(-3,4):
        if 0 <= (colonne + k) and (colonne + k) < colonnes:
            if couleur == grille[ligne][colonne+k]:
                compteur += 1
            else:
                compteur = 0
            if compteur == 4:
                return True
    return False

def verifier_diagonale(ligne, colonne, couleur):
    """verifie si un joueur a gagné en diagonale"""
    compteur = 0
    for k in range(-3, 4):
        if (0 <= (colonne + k) and (colonne + k) < colonnes) and (0 <= (ligne + k) and (ligne + k) < len(grille)):
            if couleur == grille[ligne+k][colonne+k]:
                compteur += 1
            else:
                compteur = 0
            if compteur == 4:
                return True 
    compteur = 0
    for k in range(-3, 4):
        if (0 <= (colonne + k) and (colonne + k) < colonnes) and (0 <= (ligne - k) and (ligne - k) < len(grille)):
            if couleur == grille[ligne-k][colonne+k]:
                compteur += 1
            else:
                compteur = 0
            if compteur == 4:
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
    tk.Label(fenetre2, text=message_victoire, fg=joueur["couleur"]).grid()
    tk.Button(fenetre2, text="Recommencer", command=lambda: recommencer(fenetre2)).grid()
    tk.Button(fenetre2, text="Fermer", command=root.destroy).grid()  #enft, fallait passer fenetre2 comme argument

def match_nul():#la fonction marche, mais c'est pas beau dutout...
    """affiche une fenetre de match nul"""
    global jeu_actif
    if all(None not in ligne for ligne in grille):
        jeu_actif = False
        fenetre3 = tk.Toplevel(root)
        fenetre3.title("Match nul !")
        label = tk.Label(fenetre3, text="Match nul !", fg="orange")
        label.grid(column=1, row=0, padx=50)
        label2 = tk.Label(fenetre3, text="Personne n'a gagné. Sélectionnez une option:", fg="orange")
        label2.grid(column=1, row=1, padx=50)
        bouton_recommencer = tk.Button(fenetre3, text="Recommencer", command=lambda: recommencer(fenetre3))
        bouton_recommencer.grid(column=0, row=1, padx=10, pady=10)
        bouton_fermer = tk.Button(fenetre3, text="Fermer", command=root.destroy)
        bouton_fermer.grid(column=1, row=1, padx=50)

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

    fichier.write(f"{joueurs[0]['nom']}-{joueurs[0]['couleur']}\n")
    fichier.write(f"{joueurs[1]['nom']}-{joueurs[1]['couleur']}\n")

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
    global joueur_actuel
    global lignes
    global colonnes
    global grille
    global jeu_actif
    fichier=open("savegame/savegame.txt", "r")
    li=fichier.readlines()

    joueur_actuel_sauvegarde=li[0].strip()
    if int(joueur_actuel_sauvegarde)==0:
        joueur_actuel=joueurs[0]
    elif int(joueur_actuel_sauvegarde)==1:
        joueur_actuel=joueurs[1]

    ligne_joueur_0=li[1].strip().split("-")
    ligne_joueur_1=li[2].strip().split("-")
    joueurs[0]["nom"]=ligne_joueur_0[0]
    joueurs[0]["couleur"]=ligne_joueur_0[1]
    joueurs[1]["nom"]=ligne_joueur_1[0]
    joueurs[1]["couleur"]=ligne_joueur_1[1]

    dimensions=li[3].strip().split("x")
    lignes=int(dimensions[0])
    colonnes=int(dimensions[1])

    grille_sv = [["#" for _ in range(colonnes)] for _ in range(lignes)]
    cpt = 0
    while cpt < lignes:
        ligne_save = li[4 + cpt].strip()
        j = 0
        while j < colonnes:
            if ligne_save[j] == "0":
                grille_sv[cpt][j] = joueurs[0]
            elif ligne_save[j] == "1":
                grille_sv[cpt][j] = joueurs[1]
            elif ligne_save[j] == "#":
                grille_sv[cpt][j] = None
            j += 1
        cpt += 1
    grille=grille_sv
    fichier.close()
    tk.messagebox.showinfo("Partie chargée !",f"Le joueur actuel est {joueur_actuel['nom']}.")
    return grille, joueurs, joueur_actuel, lignes, colonnes


def lancer_jeu(charger_partie=False):
    global lignes
    global colonnes
    global joueur_actuel
    global grille
    global jeu_actif
    global canvas
    global canvas_frame

    # On doit rénitialiser tout par défaut avant de récupérer les informations de la config
    #sinon, soucis au niveau de nouvelle partie après avoir chargé partie
    if not charger_partie:
        if not joueurs[0].get("nom"):
            joueurs[0]["nom"] = "Joueur 1"
        if not joueurs[1].get("nom"):
            joueurs[1]["nom"] = "Joueur 2"

        if not joueurs[0].get("couleur"):
            joueurs[0]["couleur"] = "red"
        if not joueurs[1].get("couleur"):
            joueurs[1]["couleur"] = "yellow"

        if not joueurs[0].get("Joker"):
            joueurs[0]["Joker"] = True
        if not joueurs[1].get("Joker"):
            joueurs[1]["Joker"] = True
    # On vérifie que les entrées sont valides, sinon on applique direct les valeurs par défaut
    #En fait, ya un soucis avec la gestion des données par défaut. Le jeu n'applique pas les paramètres sans ça
        if not entree_lignes.get().isdigit():
            lignes = 6
        else:
            lignes = int(entree_lignes.get())

        if not entree_colonnes.get().isdigit():
            colonnes = 7
        else:
            colonnes = int(entree_colonnes.get())

    
    if charger_partie:
        charger()
    else:
        if not entree_lignes.get().isdigit() or not entree_colonnes.get().isdigit():
            lignes = 6
            colonnes = 7
        else:
            lignes = int(entree_lignes.get())
            colonnes = int(entree_colonnes.get())
        joueurs[0]["nom"] = entree_nom_joueur1.get()
        joueurs[1]["nom"] = entree_nom_joueur2.get()
        joueur_actuel = matchmaking()
        grille[:] = [[None for _ in range(colonnes)] for _ in range(lignes)]

    jeu_actif=True
    fenetre_jeu = tk.Toplevel()
    fenetre_jeu.title("Puissance 4")
    canvas_frame = tk.Frame(fenetre_jeu)
    canvas_frame.grid()
    canvas = tk.Canvas(canvas_frame, width=colonnes * dim_case, height=lignes * dim_case, bg="#2C3E50")
    canvas.grid()
    canvas.bind("<Button-1>", interagir_jeu)
    canvas.bind("<Button-3>", utiliser_joker)
    afficher_grille()

    bouton_sauvegarde = tk.Button(fenetre_jeu, text="Sauvegarder", command=sauvegarder)
    bouton_sauvegarde.grid(pady=5)

root.mainloop()
