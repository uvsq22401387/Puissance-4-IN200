from imports import *
from puissance4 import interagir_jeu
from front import afficher_grille

# Ajout du canvas à la fenêtre
canvas.pack()
afficher_grille()
canvas.bind("<Button-1>", interagir_jeu)
root.mainloop()
