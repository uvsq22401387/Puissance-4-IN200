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

joueur_actuel = rd.choice(joueurs)

canvas = tk.Canvas(root, width=colonnes * dim_case, height=lignes * dim_case, bg="#2C3E50")


