import customtkinter as ctk
import json
import os
import game
import menu
frame_level_select = [
    [6+1, 1, 1, 4+1, 1, 1, 3+1, 1, 1, 2+1],
    [0,   0, 0, 1,   0, 0, 1,   0, 0, 1   ],
    [0,   0, 0, 1,   0, 0, 1,   0, 0, 1   ],
    [0,   0, 0, 7+1, 0, 0, 1,   0, 0, 1+1 ],
    [0,   0, 0, 1,   0, 0, 1,   0, 0, 0   ],
    [0,   0, 0, 1,   0, 0, 1,   0, 0, 0   ],
    [9+1, 1, 1, 8+1, 1, 1, 5+1, 0, 0, 0   ],
]
TAILLE_CELLULE = 100
COLONNES = len(frame_level_select[0])
LIGNES   = len(frame_level_select)
COULEUR_GRILLE   = "#1a1a2e"
COULEUR_BORD     = "#16213e"
COULEUR_JOUEUR   = "#00FF88"
COULEUR_INTERDIT = "#0a0a0a"   # ← couleur des cases interdites (0)
COULEUR_CHEMIN   = "#2a2a4e"   # ← couleur des cases autorisées (pas 0)
largeur_canvas = COLONNES * TAILLE_CELLULE
hauteur_canvas = LIGNES   * TAILLE_CELLULE

def lv_select_screen(app):
    dossier = os.path.dirname(__file__)
    fichier_setting = os.path.join(dossier, "settings.json")
    fichier_instance = os.path.join(dossier, "Save\\instance.json")
    with open(fichier_setting, "r", encoding="utf-8") as jason : setting = json.load(jason)
    with open(fichier_instance, "r", encoding="utf-8") as jason : instance = json.load(jason)
    position_depart = None
    # 1+1 = 2 = niveau 1
    for l in range(LIGNES):
        for c in range(COLONNES):
            if frame_level_select[l][c] == 2:   
                position_depart = (l, c)
                break
        if position_depart:break
    # Si on trouve pas le niveau 1, on met (0,0) par défaut
    joueur = {
        "ligne"  : position_depart[0] if position_depart else 0,
        "colonne": position_depart[1] if position_depart else 0,
    }
    titre = ctk.CTkLabel(
        app,
        text="Selectionner un niveau",
        font=("Copperplate Gothic Bold", 44, "bold")
    ).pack(pady=10)
    info = ctk.CTkLabel(
        app,
        text="",
        font=("Copperplate Gothic Bold", 24, "bold")
    )
    info.pack(pady=10)
    canvas = ctk.CTkCanvas(
        app,
        width=largeur_canvas,
        height=hauteur_canvas,
        bg=COULEUR_GRILLE,
        highlightthickness=0
    )
    canvas.pack(pady=10)

    def find_key(dico, value):
        for key, val in dico.items():
            if val == value:
                return key
        return None

    def dessiner_grille():
        global setting
        with open(fichier_setting, "r", encoding="utf-8") as jason:
            setting = json.load(jason)
        canvas.delete("all")
        for ligne in range(LIGNES):
            for colonne in range(COLONNES):
                x1 = colonne * TAILLE_CELLULE
                y1 = ligne   * TAILLE_CELLULE
                x2 = x1 + TAILLE_CELLULE
                y2 = y1 + TAILLE_CELLULE
                valeur = frame_level_select[ligne][colonne]
                if ligne == joueur["ligne"] and colonne == joueur["colonne"]:couleur = COULEUR_JOUEUR
                elif valeur == 0: couleur = COULEUR_INTERDIT
                else:couleur = COULEUR_CHEMIN
                canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=couleur,
                    outline=COULEUR_BORD,
                    width=1
                )
                if valeur > 1 and not (ligne == joueur["ligne"] and colonne == joueur["colonne"]):
                    canvas.create_text(
                        (x1 + x2) // 2,
                        (y1 + y2) // 2,
                        text=str(valeur - 1),
                        fill="white",
                        font=("Copperplate Gothic Bold", 24, "bold")
                    )
        marge = 8
        x1 = joueur["colonne"] * TAILLE_CELLULE + marge
        y1 = joueur["ligne"]   * TAILLE_CELLULE + marge
        x2 = x1 + TAILLE_CELLULE - 2 * marge
        y2 = y1 + TAILLE_CELLULE - 2 * marge
        canvas.create_oval(
            x1, y1, x2, y2,
            fill=COULEUR_JOUEUR,
            outline="white",
            width=2
        )
        valeur_case = frame_level_select[joueur["ligne"]][joueur["colonne"]]
        if valeur_case > 1:info.configure(text=f"Niveau {valeur_case - 1} sélectionnable   << {find_key(setting["keys"], "Attack").upper()} >>")
        else:info.configure(text=f"Chemin...")

    def est_accessible(ligne, colonne):
        if ligne < 0 or ligne >= LIGNES:return False
        if colonne < 0 or colonne >= COLONNES:return False
        if frame_level_select[ligne][colonne] == 0:return False
        return True
    
    def selectionner_niveau():
        valeur = frame_level_select[joueur["ligne"]][joueur["colonne"]]
        if valeur > 1:
            numero_niveau = valeur - 1
            if instance["lv"] >= numero_niveau:
                print(f"Lancement du niveau {numero_niveau} !")
                for widget in app.winfo_children():
                    widget.destroy()
                def retour_menu():
                    menu.menu(app)
                def retour_selection():
                    for widget in app.winfo_children():
                        widget.destroy()
                    lv_select_screen(app)
                game.start(
                    app,
                    lv                  = numero_niveau,
                    on_quit             = retour_menu,
                    on_level_complete   = retour_selection
                )
            else: return
        else: return

    def deplacer(event):
        global setting
        with open(fichier_setting, "r", encoding="utf-8") as jason:
            setting = json.load(jason)
        touche = event.keysym
        if touche in setting["keys"] and setting["keys"][touche] == "Attack":
            selectionner_niveau()
            return
        if touche not in setting["keys"]:return
        direction = setting["keys"][touche]
        nouvelle_ligne   = joueur["ligne"]
        nouvelle_colonne = joueur["colonne"]
        if direction == "forward":nouvelle_ligne -= 1
        elif direction == "backward":nouvelle_ligne += 1
        elif direction == "right":nouvelle_colonne += 1
        elif direction == "left":nouvelle_colonne -= 1
        if est_accessible(nouvelle_ligne, nouvelle_colonne):
            joueur["ligne"]   = nouvelle_ligne
            joueur["colonne"] = nouvelle_colonne
            dessiner_grille()

    app.bind("<Key>", deplacer)
    dessiner_grille()
    
