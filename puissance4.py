import tkinter as tk
import random as rd



root = tk.Tk()
root.title("Puissance 4")

jeu_actif = True
lignes = 6
colonnes = 7
dim_case = 80
grille = [[None] * colonnes for _ in range(lignes)]

joueurs = [
    {"nom": "Joueur 1", "couleur": "red"},
    {"nom": "Joueur 2", "couleur": "yellow"}
]

def matchmaking():
    joueur_actuel = rd.choice(joueurs)
    return joueur_actuel
joueur_actuel = matchmaking()


def selection_joueur():
    global joueur_actuel
    if joueur_actuel == joueurs[0]:
        joueur_actuel = joueurs[1]
    else:
        joueur_actuel = joueurs[0] 

def afficher_grille():
    canvas.delete("all")
    for i in range(lignes):
        for j in range(colonnes):
            x1 = j * dim_case + 5
            y1 = i * dim_case + 5
            x2 = x1 + dim_case - 10
            y2 = y1 + dim_case - 10
            if grille[i][j] is None:
                couleur = "white"
            else:
                case = grille[i][j]  
                couleur = case["couleur"]
            canvas.create_oval(x1, y1, x2, y2, fill=couleur, outline="black", width=4)

def interagir_jeu(event):
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
                #if verifier_victoire(ligne, colonne):
                    #fenetre_congrats(joueur_actuel)
                    #jeu_actif = False
                    #return
                selection_joueur()
                return

#def verifier_victoire():
    #pass

canvas = tk.Canvas(root, width=colonnes * dim_case, height=lignes * dim_case, bg="#2C3E50")
canvas.pack()
afficher_grille()
canvas.bind("<Button-1>", interagir_jeu)
root.mainloop()

"""
RAPPEL:
Répartition des tâches pour le projet Puissance 4 :
1. **Anis** : Doit se charger de l'interaction joueur-jeu ainsi que de la configuration de la partie.
   - La configuration sera faite plus tard et partagée entre 4 personnes.

"""
