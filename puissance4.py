import tkinter as tk
import random



root = tk.Tk()
root.title("Puissance 4")
jeu_actif = True
lignes = 6
colonnes = 7
dim_case = 80
grille = [[None] * colonnes for _ in range(lignes)]


#gestion des joueurs à ajouter par ghofrane pour que 'couleur' soit reconnu


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


canvas = tk.Canvas(root, width=colonnes * dim_case, height=lignes * dim_case, bg="#2C3E50")
canvas.pack()
root.mainloop()