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
    {"nom": "Joueur 2", "couleur": "yellow"}]

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
            x1, y1 = j * dim_case + 5, i * dim_case + 5
            x2, y2 = x1 + dim_case - 10, y1 + dim_case - 10
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
#il manque le travail de pierre faut qu'il se bouge :)
    #pass

def fenetre_congrats(joueur):
    global jeu_actif
    jeu_actif = False
    
    fenetre2 = tk.Toplevel(root)
    fenetre2.title("Victoire !")
    message_victoire = joueur["nom"] + " a gagné !"
    label = tk.Label(fenetre2, text=message_victoire,font=("Comic Sans MS", 16), fg=joueur["couleur"])
    label.grid(column=1, row=0, padx=50)
    
    #doit ajouter le bouton recommencer
    
    bouton_fermer = tk.Button(fenetre2, text="Fermer", command=root.destroy)
    bouton_fermer.grid(column=1, row=1, padx=50)

#def recommencer():
    #pass

canvas = tk.Canvas(root, width=colonnes * dim_case, height=lignes * dim_case, bg="#2C3E50")
canvas.pack()
afficher_grille()
canvas.bind("<Button-1>", interagir_jeu)
root.mainloop()
