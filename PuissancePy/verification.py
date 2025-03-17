from imports import *

def verifier_vertical(ligne, colonne, couleur):
    compteur = 0
    for k in range(-3, 4):
        if 0 > (colonne + k) or (colonne + k) >= len(grille[0]):
            break
        if couleur == grille[ligne+k][colonne]:
            compteur += 1
        else:
            compteur = 0
        if compteur == 4:
            return True
    return False


def verifier_horizontal(ligne, colonne, couleur):
    compteur = 0
    for k in range(-3,4):
        if 0 > (colonne + k) or (colonne + k) >= len(grille[0]):
            break
        if couleur == grille[ligne][colonne+k]:
            compteur += 1
        else:
            compteur = 0
        if compteur == 4:
            return True
    return False

def verifier_diagonale(ligne, colonne, couleur):
    compteur = 0
    for k in range(-3, 4):
        if 0 > (colonne + k) or (colonne + k) >= len(grille[0]) or 0 > (ligne + k) or (ligne + k) >= len(grille):
            break
        if couleur == grille[ligne+k][colonne+k]:
            compteur += 1
        else:
            compteur = 0
        if compteur == 4:
            return True 
    compteur = 0
    for k in range(-3, 4):
        if 0 > (colonne + k) or (colonne + k) >= len(grille[0]) or 0 > (ligne + k) or (ligne + k) >= len(grille):
            break
        if couleur == grille[ligne-k][colonne+k]:
            compteur += 1
        else:
            compteur = 0
        if compteur == 4:
            return True 
    return False 


def verifier_victoire(ligne, colonne):
    couleur = grille[ligne][colonne]
    if verifier_vertical(ligne, colonne, couleur) or verifier_horizontal(ligne, colonne, couleur) or verifier_diagonale(ligne, colonne, couleur):
        return True
    return False