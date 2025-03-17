from imports import *

def afficher_grille():
    """Affiche la grille avec les pions."""
    canvas.delete("all")
    for i in range(lignes):
        for j in range(colonnes):
            x1, y1 = j * dim_case + 5, i * dim_case + 5
            x2, y2 = x1 + dim_case - 10, y1 + dim_case - 10
            couleur = "white" if grille[i][j] is None else grille[i][j]["couleur"]
            canvas.create_oval(x1, y1, x2, y2, fill=couleur, outline="black", width=4)

def fenetre_congrats(joueur):
    """Affiche la fenêtre de victoire."""
    global jeu_actif
    jeu_actif = False
    top = tk.Toplevel()
    top.title("Félicitations")
    label = tk.Label(top, text=f"{joueur['nom']} a gagné !", font=("Arial", 20))
    label.pack(pady=20)
    bouton_rejouer = tk.Button(top, text="Rejouer", command=rejouer)
    bouton_rejouer.pack(pady=10)

def rejouer():
    """Réinitialise la partie."""
    global jeu_actif, grille
    jeu_actif = True
    grille = [[None] * colonnes for _ in range(lignes)]
    selection_joueur()
    afficher_grille()
