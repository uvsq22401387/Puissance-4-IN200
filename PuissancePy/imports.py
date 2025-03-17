import tkinter as tk
import random as rd

# Création de la fenêtre principale
root = tk.Tk()
root.title("Puissance 4")

# Définition des constantes
lignes = 7
colonnes = 7
dim_case = 80
jeu_actif = True

# Grille vide
grille = [[None] * colonnes for _ in range(lignes)]

# Définition des joueurs
joueurs = [
    {"nom": "Joueur 1", "couleur": "red"},
    {"nom": "Joueur 2", "couleur": "yellow"}
]

# Sélection du joueur actuel (par défaut, Joueur 1)
joueur_actuel = joueurs[0]

# Création du canvas
canvas = tk.Canvas(root, width=colonnes * dim_case, height=lignes * dim_case, bg="#2C3E50")

def selection_joueur():
    """Change de joueur après chaque tour."""
    global joueur_actuel
    joueur_actuel = joueurs[1] if joueur_actuel == joueurs[0] else joueurs[0]
    print("switching")
