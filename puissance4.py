import tkinter as tk
import random as rd
from tkinter import *

root = tk.Tk()
root.title("Puissance 4")

# Variables globales
jeu_actif = True
lignes = 6
colonnes = 7
dim_case = 80
grille = [[None] * colonnes for _ in range(lignes)]
joueurs = [
    {"nom": "Joueur 1", "couleur": "red"},
    {"nom": "Joueur 2", "couleur": "yellow"}]
canvas = tk.Canvas(root, width=colonnes * dim_case, height=lignes * dim_case, bg="#2C3E50")

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


def fenetre_congrats(joueur):#ici aussi, on doit restyliser
    """affiche une fenetre de victoire lorsqu'un joueur gagne""" 
    global jeu_actif
    jeu_actif = False
    
    fenetre2 = tk.Toplevel(root)
    fenetre2.title("Victoire !")
    message_victoire = joueur["nom"] + " a gagné !"
    label = tk.Label(fenetre2, text=message_victoire,font=("Comic Sans MS", 16), fg=joueur["couleur"])
    label.grid(column=1, row=0, padx=50)
    
    bouton_recommencer = tk.Button(fenetre2, text="Recommencer", command=lambda: recommencer(fenetre2))
    bouton_recommencer.grid(column=0, row=1, padx=10, pady=10)
    bouton_fermer = tk.Button(fenetre2, text="Fermer", command=root.destroy) #enft, fallait passer fenetre2 comme argument
    bouton_fermer.grid(column=1, row=1, padx=50)

def match_nul():#la fonction marche, mais c'est pas beau dutout...
    """affiche une fenetre de match nul"""
    global jeu_actif
    if all(None not in ligne for ligne in grille):
        jeu_actif = False
        fenetre3 = tk.Toplevel(root)
        fenetre3.title("Match nul !")
        label = tk.Label(fenetre3, text="Match nul !", font=("Comic Sans MS", 16, "bold"), fg="orange")
        label.grid(column=1, row=0, padx=50)
        label2 = tk.Label(fenetre3, text="Personne n'a gagné. Sélectionnez une option:", font=("Comic Sans MS", 14), fg="orange")
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
    if fenetre!=root:
        fenetre.destroy()
    afficher_grille()


def sauvegarder():
    '''la fonction se charge de sauvegarder la partie en cours'''
    #seul problème c'est que le dossier doit préexister. j'ai crée le dossier savegame sur github
    fichier = open("savegame/savegame.txt", "w")
    couleur_j0=joueurs[0]["couleur"]
    couleur_j1=joueurs[1]["couleur"]

    if joueur_actuel == joueurs[0]:
        fichier.write("0\n")
    else:
        fichier.write("1\n")
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
    global grille
    global jeu_actif
    fichier=open("savegame/savegame.txt", "r")
    li=fichier.readlines()
    fichier.close()

    joueur_actuel_sauvegarde=li[0].strip()
    if int(joueur_actuel_sauvegarde)==0:
        joueur_actuel=joueurs[0]
    elif int(joueur_actuel_sauvegarde)==1:
        joueur_actuel=joueurs[1]

    grille_sv=[["#"]*colonnes for i in range(lignes)] 
    cpt=0
    i=1
    while i<len(li):
        ligne_save=li[i].strip()
        len_l=len(ligne_save)
        j=0
        while j<len_l:
            if ligne_save[j]=="0":
                grille_sv[cpt][j]=joueurs[0]
            elif ligne_save[j]=="1":
                grille_sv[cpt][j]=joueurs[1]
            elif ligne_save[j]=="#":
                grille_sv[cpt][j]=None
            j+= 1
        cpt+= 1
        i+= 1
    grille=grille_sv
    
    afficher_grille()
    tk.messagebox.showinfo("Partie chargée !",f"Le joueur actuel est {joueur_actuel['nom']}.")

'''ajout des boutons à la fenêtre principale'''
button_frame = tk.Frame(root)
button_frame.pack()
bouton_sauvegarder = tk.Button(button_frame, text="Sauvegarder", command=sauvegarder)
bouton_sauvegarder.grid(row=0, column=1, padx=5)
bouton_sauvegarder = tk.Button(button_frame, text="Charger", command=charger)
bouton_sauvegarder.grid(row=0, column=2, padx=5)
bouton_nouveau = tk.Button(button_frame, text="Nouvelle Partie", command=lambda: recommencer(root))
bouton_nouveau.grid(row=0, column=0, padx=5)


#crée la fenêtre 
canvas.pack()
afficher_grille()
canvas.bind("<Button-1>", interagir_jeu)
root.mainloop()
