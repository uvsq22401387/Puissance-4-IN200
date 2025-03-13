import tkinter as tk
import random



root = tk.Tk()
root.title("Puissance 4")
jeu_actif = True



canvas = tk.Canvas(root, width=colonnes * dim_case, height=lignes * dim_case, bg="#2C3E50")
canvas.pack()
root.mainloop()