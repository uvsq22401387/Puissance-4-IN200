from imports import *
from verification import *
from front import afficher_grille, fenetre_congrats  # 🔥 Import nécessaire

def interagir_jeu(event):
    """Gère le clic de l'utilisateur et place un pion."""
    global joueur_actuel, jeu_actif

    if not jeu_actif:
        return

    colonne = event.x // dim_case
    for i in range(lignes - 1, -1, -1):
        if grille[i][colonne] is None:
            grille[i][colonne] = joueur_actuel
            afficher_grille()  # ✅ Maintenant, cette fonction est bien importée !
            if verifier_victoire(i, colonne):
                fenetre_congrats(joueur_actuel)  # ✅ Importé aussi pour éviter une autre erreur
                jeu_actif = False
                return
            selection_joueur()
            return

def matchmaking():
    global joueur_actuel
    joueur_actuel = rd.choice(joueurs)

matchmaking() 

