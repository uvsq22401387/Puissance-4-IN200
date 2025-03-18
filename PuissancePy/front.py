from imports import *
from puissance4 import selection_joueur
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

def recommencer():
    pass

def rejouer():
    """Réinitialise la partie."""
    global jeu_actif, grille
    jeu_actif = True
    grille = [[None] * colonnes for _ in range(lignes)]
    selection_joueur()
    afficher_grille()
