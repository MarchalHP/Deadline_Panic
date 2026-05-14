import customtkinter as ctk
from map_generator import generer_map, frame
from math import ceil
import os
import json
import random
from PIL import Image, ImageTk
import tkinter as tk
from datetime import datetime
import code_audio

TAILLE_CELLULE = 146
HUD_CELLULE = 150
COULEUR_GRILLE   = "#dd14cc"
COULEUR_BORD     = "#000000"
COULEUR_JOUEUR   = "#00FF88"
COULEUR_INTERDIT = "#df0d0d"
COULEUR_VIDE   = "transparent"
MODIF = 150
FRAME_SIZE = (16*MODIF, 9*MODIF)
CASE_SIZE = (TAILLE_CELLULE, TAILLE_CELLULE)
PLAYER_SIZE = (TAILLE_CELLULE, int(TAILLE_CELLULE*1.5))
PL = 0
ED = None
SCAPE = False
ITEM_SELECT = 1
hud_canvas = None
touch_push = set()
mobs_img = []
obj_img = []
MOBS = {}
OBJ = {}
ITEMS = []
projectiles_actifs = []
direc = "S"
pause_overlay = None
settings_overlay = None
epic = 0

class bouton: 
    def __init__(self, app, text, command, font=("Copperplate Gothic Bold", 10, "bold"),
            col_enter="white" , col_out="#FFD700"):
        self.widget = ctk.CTkButton(
            master                  = app,
            text                    = text,
            font                    = font,
            width                   = 400,
            height                  = 50,
            fg_color                = "#0d0d1a",
            hover_color             = "#0d0d1a",
            text_color              = "white",
            text_color_disabled     = "gray",
            command                 =command        
        )
        self.widget.bind("<Enter>", lambda e: self.widget.configure(text_color=col_out))
        self.widget.bind("<Leave>", lambda e: self.widget.configure(text_color=col_enter))
    def place(self, x=None, y=None, anchor=None):
        self.widget.place(x=x, y=y, anchor=anchor)
        return self
    def pack(self, padx=None, pady=None, anchor="center", side=None):
        self.widget.pack(padx=padx, pady=pady, anchor=anchor, side=side)
        return self
    def cacher(self):
        self.widget.place_forget()
    def destroy(self):
        self.widget.destroy()
    def place_center(self,x=None, y=None):
        w = self.widget.cget("width")
        h = self.widget.cget("height")
        self.widget.place(
            x=x - w//2,
            y=y - h//2,
            anchor="center"
        )
        return self

class entity:
    def __init__(self, max_heart, position, map_pos, type, id):
        self.max_heart       = max_heart
        self.heart           = max_heart
        self.position        = position
        self.map_pos         = map_pos
        self.alive           = True
        self.type            = type
        self.id              = id
    def degat(self, damage):
        self.heart -= damage
        if self.heart <= 0:
            self.alive = False
            return True

class hostile(entity):
    def __init__(self, type, position, id, map_pos):
        with open(os.path.join(os.path.dirname(__file__), "preset_placement.json"),     "r", encoding="utf-8") as jason : preset_class   = json.load(jason)
        max_heart = preset_class["mobs"][type]["max_heart"]
        super().__init__(max_heart, position, map_pos, type, id)
        self.speed          = preset_class["mobs"][self.type]["speed"]
        self.attaque        = preset_class["mobs"][self.type]["attaque"]
        self.type_attaque   = preset_class["mobs"][self.type]["type_attaque"]
        self.porter         = preset_class["mobs"][self.type]["porter"]
    
class obj(entity):
    def __init__(self, max_heart, position, map_pos, type, id):
        with open(os.path.join(os.path.dirname(__file__), "preset_placement.json"), "r", encoding="utf-8") as jason : preset_class = json.load(jason)
        super().__init__(max_heart, position, map_pos, type, id)
        self.loot_table     = preset_class["loot_table"][self.type]
        return
    def loot(self):
        looth = random.choice(self.loot_table)
        if looth != "Nothing":
            ITEMS.append(item(
                type        = looth,
                position    = self.position,
                map_pos     = self.map_pos
            ))

class item:
    def __init__(self, position, map_pos, type):
        self.position   = position
        self.map_pos    = map_pos
        self.type       = type
        self.img        = None
    def place(self, canvas):
        self.canvas = canvas
        img = item_texture[f"{self.type}.png"]
        self.img = canvas.create_image(
            (self.position[1] * TAILLE_CELLULE) + startx,
            (self.position[0] * TAILLE_CELLULE) + starty,
            anchor="nw",
            image=img
        )
    def recup(self):
        global ITEMS
        ITEMS.remove(self)
        self.canvas.delete(self.img)

class projectile:
    def __init__(self, li, co, direction, degats, vitesse, type):
        self.li         = li
        self.co         = co
        self.direction  = direction
        self.degats     = degats
        self.vitesse    = vitesse
        self.type       = type
        self.canvas_id  = None
        self.actif      = True
        self.image_ref  = None

def start(app, lv=1, position_frame=None, position_map=[5, 5], init_map=None, on_quit=None):
    dossier = os.path.dirname(__file__)
    chemin_preset       = os.path.join(dossier, "preset_placement.json")
    fichier_setting     = os.path.join(dossier, "settings.json")
    fichier_instance    = os.path.join(dossier, "Save\\instance.json")
    dossier_frames      = os.path.join(dossier, "Texture\\frames")
    dossier_obj         = os.path.join(dossier, "Texture\\obj")
    dossier_player      = os.path.join(dossier, "Texture\\players")
    dossier_hud_texture = os.path.join(dossier, "Texture\\hud")
    dossier_hostile     = os.path.join(dossier, "Texture\\hostile")
    dossier_item        = os.path.join(dossier, "Texture\\item")
    with open(chemin_preset,     "r", encoding="utf-8") as jason : preset   = json.load(jason)
    with open(fichier_setting,   "r", encoding="utf-8") as jason : setting  = json.load(jason)
    with open(fichier_instance,  "r", encoding="utf-8") as jason : instance = json.load(jason)
    playlist_menu       = preset["playlists"]["playlist_menu"]
    random.seed(instance["seed"])
    if init_map: map_framed = init_map
    else:map, map_framed = generer_map(lv)
    frame_actuel = map_framed[f"{position_map}"].get_disposition()
    mob_map = map_framed[f"{position_map}"].get_mob()
    if position_frame : position_actuel = position_frame
    else:
        L_ran = random.choice(range(len(frame_actuel)))
        C_ran = random.choice(range(len(frame_actuel[L_ran])))
        SEDT = instance["seed"]
        while frame_actuel[L_ran][C_ran] != 0:
            SEDT += 1
            random.seed(SEDT)
            L_ran = random.choice(range(len(frame_actuel)))
            C_ran = random.choice(range(len(frame_actuel[L_ran])))
        position_actuel = ['B', 'T']
        position_actuel[0] = L_ran
        position_actuel[1] = C_ran
    
    def initialisation_img():
        global dic_frame, dic_obj, players, hud_texture, hostile_texture, item_texture
        dic_frame = {}
        for frame in os.listdir(dossier_frames):
                if not frame.endswith(".png"):
                    continue
                nom = frame.removesuffix(".png") + "_frame"
                img_pil = Image.open(os.path.join(dossier_frames, frame)).convert("RGBA").resize(FRAME_SIZE, Image.LANCZOS)
                photo = ImageTk.PhotoImage(img_pil)
                dic_frame[nom] = photo
        dic_obj = {}
        for obj in os.listdir(dossier_obj):
                # if not obj.endswith(".png"):
                #     continue
                img_pil = Image.open(os.path.join(dossier_obj, obj)).convert("RGBA").resize(CASE_SIZE, Image.LANCZOS)
                dic_obj[obj] = ImageTk.PhotoImage(img_pil)
        players = {}
        for i in os.listdir(dossier_player):
            img_pil = Image.open(os.path.join(dossier_player, i)).convert("RGBA").resize(PLAYER_SIZE, Image.LANCZOS)
            players[i] = ImageTk.PhotoImage(img_pil)
        hud_texture = {}
        for i in os.listdir(dossier_hud_texture):
            img_pil = Image.open(os.path.join(dossier_hud_texture, i)).convert("RGBA").resize(HUD_SIZE, Image.LANCZOS)
            hud_texture[i] = ImageTk.PhotoImage(img_pil)
        hostile_texture = {}
        for i in os.listdir(dossier_hostile):
            img_pil = Image.open(os.path.join(dossier_hostile, i)).convert("RGBA").resize(CASE_SIZE, Image.LANCZOS)
            hostile_texture[i] = ImageTk.PhotoImage(img_pil)
        item_texture = {}
        for i in os.listdir(dossier_item):
            img_pil = Image.open(os.path.join(dossier_item, i)).convert("RGBA").resize(CASE_SIZE, Image.LANCZOS)
            item_texture[i] = ImageTk.PhotoImage(img_pil)

    def clear(exceptions=[]):
        for widget in app.winfo_children():
            if widget not in exceptions:
                widget.destroy()

    def actualise_zero():
        global LX, LY, NB_COL, NB_LI, MODIF, FRAME_SIZE, HUD_X, HUD_Y, HUD_SIZE, TAILLE_CELLULE, CASE_SIZE, PLAYER_SIZE, startx, starty
        LX = app.winfo_width()
        LY = app.winfo_height()
        NB_COL = len(frame_actuel[0])
        NB_LI = len(frame_actuel)
        MODIF = int((app.winfo_width() * 0.8)//16)
        FRAME_SIZE = (16*MODIF, 9*MODIF)
        HUD_X = int(LX * 0.5)
        HUD_Y = int(LY *0.08)
        HUD_SIZE = (HUD_Y, HUD_Y)
        TAILLE_CELLULE = int(MODIF*0.97)
        CASE_SIZE = (TAILLE_CELLULE, TAILLE_CELLULE)
        PLAYER_SIZE = (TAILLE_CELLULE, int(TAILLE_CELLULE*1.5))
        startx = (LX - NB_COL * TAILLE_CELLULE)//2
        starty = (LY - NB_LI * TAILLE_CELLULE)//2
        initialisation_img()
        actualiser_frame()

    def actualiser_hud():
        global hud_canvas
        if hud_canvas : hud_canvas.destroy()
        hud_canvas = tk.Canvas(
            app,
            width=HUD_X,
            height=HUD_Y,
            bg="#1a1a2e",
            highlightthickness=0,
        )
        hud_canvas.place(x=int(LX*0.25), y=0)
        nb_ico_heart = instance["max_heart"]//2
        for i in range(nb_ico_heart):
            pv_rest = ceil(instance["heart"]) - (i * 2)
            if pv_rest >= 2:
                texture = hud_texture["heart_full.png"]
            elif pv_rest == 1:
                texture = hud_texture["heart_half.png"]
            else:
                texture = hud_texture["heart_void.png"]
            hud_canvas.create_image(
                    HUD_Y//2 + HUD_Y*i,
                    0,
                    anchor="n",
                    image=texture
                )
        nb_ico_abso = instance["max_abso"]//2
        for i in range(nb_ico_abso):
            pv_rest = ceil(instance["abso"]) - (i * 2)
            if pv_rest >= 2:
                texture = hud_texture["heart_blue.png"]
            elif pv_rest == 1:
                texture = hud_texture["heart_blue_half.png"]
            else: continue
            offset_x = HUD_Y // 2 + HUD_Y * (nb_ico_heart + i)
            hud_canvas.create_image(
                offset_x,
                0,
                anchor="n",
                image=texture
            )
        hud_canvas.create_image(
                (HUD_Y // 2) + HUD_Y * (ITEM_SELECT-1 + nb_ico_heart + nb_ico_abso),
                0,
                anchor="n",
                image=hud_texture["allo.png"]
            )
        nb_ico_inv = instance["inventair"]
        for i, j in enumerate(nb_ico_inv):
            texture = item_texture[f"{j}.png"]
            offset_x = (HUD_Y // 2) + HUD_Y * (i + nb_ico_heart + nb_ico_abso)
            hud_canvas.create_image(
                offset_x,
                0,
                anchor="n",
                image=texture
            )

    def actualiser_frame():
        global OBJ, obj_img
        nonlocal frame_actuel
        frame_actuel    = map_framed[f"{position_map}"].get_disposition()
        frame_id        = map_framed[f"{position_map}"].get_id()
        for y in range(len(frame_actuel)):
            for x in range(len(frame_actuel[y])):
                if frame_actuel[y][x] == 0: continue
                if f"{frame_actuel[y][x]}_{frame_id[y][x]}" not in OBJ:
                    OBJ[f"{frame_actuel[y][x]}_{frame_id[y][x]}"] = obj(
                        type        = frame_actuel[y][x],
                        id          = frame_id[y][x],
                        position    = [y, x],
                        map_pos     = [position_map[0], position_map[1]],
                        max_heart   = 3
                    )
        clear()
        obj_img = []
        zone = map_framed[f'{position_map}'].get_zone()
        canvas = tk.Canvas(
            app,
            width=LX,
            height=LY,
            bg="#1a1a2e",
            highlightthickness=0
        )
        canvas.place(x=0, y=0)
        fond_photo = dic_frame[zone + "_frame"]
        canvas.create_image(
            app.winfo_width() // 2,
            app.winfo_height() // 2,
            anchor="center",
            image=fond_photo
        )
        canvas._fond = fond_photo
        for id in OBJ:
            if OBJ[id].alive and OBJ[id].map_pos == position_map:
                img = dic_obj[f"{OBJ[id].type}.png"]
                objc = canvas.create_image(
                    (OBJ[id].position[1] * TAILLE_CELLULE) + startx,
                    (OBJ[id].position[0] * TAILLE_CELLULE) + starty,
                    anchor="nw",
                    image=img
                )
                obj_img.append(objc)
        if ITEMS:
            for i in ITEMS:
                if i.map_pos == position_map:
                    i.place(canvas)

        app._canvas_jeu = canvas
        actualiser_mobs()
        actualise_player(canvas) 
        actualiser_hud()
        # code_audio.afficher(app=app, bg_col="#1A1A2E")

    def actualiser_mobs():
        global mobs_img, MOBS
        nonlocal mob_map
        mob_map = map_framed[f"{position_map}"].get_mob()
        for i in mob_map:
            if f"{mob_map[i][0]}_{i}" not in MOBS:
                MOBS[f"{mob_map[i][0]}_{i}"] = hostile(
                    type=mob_map[i][0],
                    id=i,
                    position=mob_map[i][1],
                    map_pos=position_map
                )
        canvas = app._canvas_jeu
        if mobs_img:
            for mob_id in mobs_img:canvas.delete(mob_id)
        mobs_img = []
        for id in MOBS:
            if MOBS[id].alive and MOBS[id].map_pos == position_map:
                img = hostile_texture[f"{MOBS[id].type}S.png"]
                CO = MOBS[id].position.split(",")
                mob = canvas.create_image(
                    (int(CO[0]) * TAILLE_CELLULE) + startx,
                    (int(CO[1]) * TAILLE_CELLULE) + starty,
                    anchor="nw",
                    image=img
                )
                mobs_img.append(mob)
        actualise_player(canvas)
    
    def actualise_player(canvas):
        global PL
        if PL:
            canvas.delete(PL)
        skin = str(instance["character"])
        img  = players[f"player_{skin}{direc}.png"]
        PL   = canvas.create_image(
            (position_actuel[1] * TAILLE_CELLULE) + startx,
            ((position_actuel[0] * TAILLE_CELLULE) + starty) - int(TAILLE_CELLULE * 0.5),
            anchor="nw",
            image=img
        )

    def change_frame(direction):
        nonlocal position_map, frame_actuel, position_actuel

        if direction == "forward":
            position_map = [position_map[0] - 1, position_map[1]]
        elif direction == "backward":
            position_map = [position_map[0] + 1, position_map[1]]
        elif direction == "right":
            position_map = [position_map[0], position_map[1] + 1]
        elif direction == "left":
            position_map = [position_map[0], position_map[1] - 1]

        cle = f"{position_map}"
        if cle not in map_framed:
            popup("Porte fermé", 1000, "yellow")
            if direction == "forward":   position_map[0] += 1
            elif direction == "backward":position_map[0] -= 1
            elif direction == "right":   position_map[1] -= 1
            elif direction == "left":    position_map[1] += 1
            return

        frame_actuel = map_framed[cle].get_disposition()

        NB_LI_new  = len(frame_actuel)
        NB_COL_new = len(frame_actuel[0])

        if direction == "forward":
            ligne = NB_LI_new - 1
            col = max(0, min(position_actuel[1], NB_COL_new - 1))
            while frame_actuel[ligne][col] != 0 and col < NB_COL_new - 1:
                col += 1

        elif direction == "backward":
            ligne = 0
            col = max(0, min(position_actuel[1], NB_COL_new - 1))
            while frame_actuel[ligne][col] != 0 and col < NB_COL_new - 1:
                col += 1

        elif direction == "right":
            col = 0
            ligne = max(0, min(position_actuel[0], NB_LI_new - 1))
            while frame_actuel[ligne][col] != 0 and ligne < NB_LI_new - 1:
                ligne += 1

        elif direction == "left":
            col = NB_COL_new - 1
            ligne = max(0, min(position_actuel[0], NB_LI_new - 1))
            while frame_actuel[ligne][col] != 0 and ligne < NB_LI_new - 1:
                ligne += 1

        position_actuel = [ligne, col]
        actualiser_frame()
        if LX != app.winfo_width() or LY != app.winfo_height():
            actualise_zero()
        move(position_actuel, direction)
        canvas = app._canvas_jeu
        actualise_player(canvas)

    def popup(txt, duree, color):
        LX = app.winfo_width()
        LY = app.winfo_height()
        if color == "red":
            txcolor = "#000000"
            fgcolor = "#ff0000"
        elif color == "white":
            txcolor = "#000000"
            fgcolor = "#ffffff"
        elif color == "yellow":
            txcolor = "#000000"
            fgcolor = "#FFFF00"
        elif color == "green":
            txcolor = "#000000"
            fgcolor = "#00ff00"
        elif color == "blue":
            txcolor = "#FFFFFF"
            fgcolor = "#0000ff"
        else:
            txcolor = "#FFFFFF"
            fgcolor = "#000000"
        fenetre_popup = ctk.CTkFrame(
            app,
            fg_color        = fgcolor,
            corner_radius   = 15,
            border_width    = 2,
        )
        fenetre_popup.place(
            x       = int(LX*0.5),
            y       = int(LY*0.9),
            anchor  = "center"
        )
        ctk.CTkLabel(
            fenetre_popup,
            text        = txt,
            font        = ("Copperplate Gothic Bold", int(LY*0.03), "bold"),
            text_color  = txcolor,
            fg_color    = "transparent",
            padx        = 30,
            pady        = 20
        ).pack()
        app.after(duree, fenetre_popup.destroy)
        return fenetre_popup

    def accessible(L , C):
        nonlocal mob_map
        mob_map = map_framed[f"{position_map}"].get_mob()
        if L < 0 or L >= NB_LI:return False
        if C < 0 or C >= NB_COL:return False
        for id in OBJ:
            if OBJ[id].position == [L, C] and OBJ[id].alive and OBJ[id].map_pos == position_map:
                return False
        for id in MOBS:
            if f"{C}" in MOBS[id].position.split(",")[0] and f"{L}" in MOBS[id].position.split(",")[1] and MOBS[id].alive and MOBS[id].map_pos == position_map:
                return False
        return True

    def move(position, direction="forward"):
        global PL, direc
        skin = str(instance["character"])
        situation = {"forward" : "N", "backward" : "S", "right" : "E", "left" : "W"}
        direc = situation[direction]
        img = players[f"player_{skin}{direc}.png"]
        canvas = app._canvas_jeu
        if PL : canvas.delete(PL)
        PL = canvas.create_image(
            (position[1] * TAILLE_CELLULE) + startx,
            ((position[0] * TAILLE_CELLULE) + starty) - int(TAILLE_CELLULE * 0.5),
            anchor="nw",
            image=img
        )
        if len(instance["inventair"]) < 5:
            for i in ITEMS:
                if i.position == position and i.map_pos == position_map:
                    if i.type in preset["arms"] and i.type in instance["inventair"]: pass
                    else: instance["inventair"].append(i.type)
                    i.recup()
            actualiser_hud()

    def attaque(position, direction, arm):
        if arm in preset["arms"]:
            cases_attaquer = []
            li, co = position[0], position[1]
            if preset["arms"][arm]["type_attaque"] == "corp_a_corp":
                for _ in range(preset["arms"][arm]["porter"]):
                    if   direction == "N" : li -= 1
                    elif direction == "S" : li += 1
                    elif direction == "E" : co += 1
                    elif direction == "W" : co -= 1
                    if 0 <= li < NB_LI and 0 <= co < NB_COL:
                        cases_attaquer.append((li, co))
                for id in MOBS:
                    if (int(MOBS[id].position.split(",")[1].strip()), int(MOBS[id].position.split(",")[0].strip())) in cases_attaquer and MOBS[id].map_pos == position_map and MOBS[id].alive:
                        MOBS[id].degat(int(preset["arms"][arm]["attaque"])*int(preset["preset_characters"][str(instance["character"])]["attaque"]))
                for id in OBJ:
                    if (OBJ[id].position[0], OBJ[id].position[1]) in cases_attaquer and OBJ[id].map_pos == position_map and OBJ[id].alive:
                        if OBJ[id].degat(int(preset["arms"][arm]["attaque"])*int(preset["preset_characters"][str(instance["character"])]["attaque"])):
                            OBJ[id].loot()
                actualiser_frame()
            elif preset["arms"][arm]["type_attaque"] == "distance":
                degats = int(preset["arms"][arm]["attaque"] * preset["preset_characters"][str(instance["character"])]["attaque"])
                vitesse_proj = int(1000 / preset["arms"][arm]["vitesse"])
                lancer_projectile(
                    li_depart = position[0],
                    co_depart = position[1],
                    direction = direction,
                    degats    = degats,
                    vitesse   = vitesse_proj,
                    type      = arm
                )
            
        elif arm in preset["items"]:
            instance["heart"]   = min(instance["heart"] + preset["items"][arm]["heart"], instance["max_heart"])
            instance["abso"]    = min(instance["abso"]  + preset["items"][arm]["abso"],  instance["max_abso"])
            instance["speed"]   += preset["items"][arm]["speed"]
            instance["defense"] += preset["items"][arm]["defense"]
            instance["attaque"] += preset["items"][arm]["attaque"]
            swipe("right")
            instance["inventair"].remove(arm)
            actualiser_hud()
            if preset["items"][arm]["tempo"] != -1:
                tempo_ms        = preset["items"][arm]["tempo"] * 1000
                speed_bonus     = preset["items"][arm]["speed"]
                defense_bonus   = preset["items"][arm]["defense"]
                attaque_bonus   = preset["items"][arm]["attaque"]
                def debuff(s=speed_bonus, d=defense_bonus, a=attaque_bonus):
                    instance["speed"]   -= s
                    instance["defense"] -= d
                    instance["attaque"] -= a
                    actualiser_hud()
                app.after(tempo_ms, debuff)
            actualiser_hud()
    
    def lancer_projectile(li_depart, co_depart, direction, degats, vitesse, type="Pen"):
        proj = projectile(li_depart, co_depart, direction, degats, vitesse, type)
        projectiles_actifs.append(proj)
        def deplacer_projectile():
            if not proj.actif: return
            canvas = app._canvas_jeu
            nouvelle_li = proj.li
            nouvelle_co = proj.co
            if   direction == "N": nouvelle_li -= 1
            elif direction == "S": nouvelle_li += 1
            elif direction == "E": nouvelle_co += 1
            elif direction == "W": nouvelle_co -= 1
            hors_grille = (
                nouvelle_li < 0 or nouvelle_li >= NB_LI or
                nouvelle_co < 0 or nouvelle_co >= NB_COL
            )
            if hors_grille:
                supprimer_projectile(proj)
                return
            for id in MOBS:
                if not MOBS[id].alive or MOBS[id].map_pos != position_map: continue
                if int(MOBS[id].position.split(",")[1].strip()) == nouvelle_li and int(MOBS[id].position.split(",")[0].strip()) == nouvelle_co:
                    MOBS[id].degat(degats)
                    actualiser_mobs()
                    return
            for id in OBJ:
                if not OBJ[id].alive or OBJ[id].map_pos != position_map: continue
                if OBJ[id].position[0] == nouvelle_li and OBJ[id].position[1] == nouvelle_co:
                    if OBJ[id].degat(degats):
                        OBJ[id].loot()
                    actualiser_frame()
                    return
                
            proj.li = nouvelle_li
            proj.co = nouvelle_co
            if proj.canvas_id:
                canvas.delete(proj.canvas_id)
            proj.image_ref = item_texture[f"{proj.type}{direction}.png"]
            proj.canvas_id = canvas.create_image(
                (proj.co * TAILLE_CELLULE) + startx,
                (proj.li * TAILLE_CELLULE) + starty,
                anchor="nw",
                image=proj.image_ref
            )
            app.after(vitesse, deplacer_projectile)
        app.after(0, deplacer_projectile)

    def supprimer_projectile(proj):
        canvas = app._canvas_jeu
        if proj.canvas_id: canvas.delete(proj.canvas_id)
        proj.actif = False
        if proj in projectiles_actifs: projectiles_actifs.remove(proj)

    def swipe(sens):
        global ITEM_SELECT
        nb_itm = len(instance["inventair"])
        if sens == "left":
            if 1 <= ITEM_SELECT < nb_itm:
                ITEM_SELECT += 1
        elif sens == "right":
            if 1 < ITEM_SELECT <= nb_itm:
                ITEM_SELECT -= 1
        actualiser_hud()

    def menu_escape(actif):
        global pause_overlay, SCAPE
        if not actif:
            SCAPE = False
            if pause_overlay:
                for widget in pause_overlay:
                    try: widget.destroy()
                    except: pass
                pause_overlay = None
            app.bind("<Key>", action)
            app.bind("<KeyRelease>", relacher)
            return
        SCAPE = True
        pause_overlay = []
        fond = tk.Canvas(
            app,
            width               = LX,
            height              = LY,
            bg                  = "#0d0d1a",
            highlightthickness  = 0
        )
        fond.place(x=0, y=0)
        pause_overlay.append(fond)
        fond.create_text(
            LX * 0.5, LY * 0.2,
            text = "DeadLine  Panic",
            fill = "#FFFFFF",
            font = ("Copperplate Gothic Bold", int(LY * 0.05), "bold")
        )
        btn_back = bouton(
            app         = app,
            text        = "Back to game",
            command     = lambda: menu_escape(False),
            font        = ("Copperplate Gothic Bold", int(LY*.04), "bold"),
            col_enter   = "white",
            col_out     = "#FFD700"
        ).place_center(LX*0.55, LY*0.4)
        pause_overlay.append(btn_back)
        btn_opt = bouton(
            app         = app,
            text        = "Options...",
            command     = lambda: menu_setting(True),
            font        = ("Copperplate Gothic Bold", int(LY*.04), "bold"),
            col_enter   = "white",
            col_out     = "#FFD700"
        ).place_center(LX*0.55, LY*.5)
        pause_overlay.append(btn_opt)
        btn_quit = bouton(
            app         = app,
            text        = "quit to title",
            command     = lambda: quit_to_title(),
            font        = ("Copperplate Gothic Bold", int(LY*.04), "bold"),
            col_enter   = "white",
            col_out     = "#FFD700"
        ).place_center(LX*0.55, LY*.6)
        pause_overlay.append(btn_quit)
        btn_quit_n_save = bouton(
            app         = app,
            text        = "Save and quit to title",
            command     = lambda: save(),
            font        = ("Copperplate Gothic Bold", int(LY*.04), "bold"),
            col_enter   = "white",
            col_out     = "#FFD700"
        ).place_center(LX*0.55, LY*.7)
        pause_overlay.append(btn_quit_n_save)
    
    def menu_setting(actif):
        nonlocal setting
        global settings_overlay, SCAPE
        if actif:
            if settings_overlay:
                for widget in settings_overlay:
                    try:
                        widget.destroy()
                    except:
                        pass
                settings_overlay = None
            with open(fichier_setting,   "r", encoding="utf-8") as jason : setting  = json.load(jason)
            settings_overlay = []
            fond_s = tk.Canvas(
                app,
                width              = LX,
                height             = LY,
                bg                 = "#0a0a1a",
                highlightthickness = 0
            )
            fond_s.place(x=0, y=0)
            settings_overlay.append(fond_s)
            fond_s.create_text(
                LX * 0.1, LY * 0.11,
                text = "Setting",
                fill = "#FFFFFF",
                font = ("Copperplate Gothic Bold", int(LY*0.02), "bold")
            )
            aff_vol = ctk.CTkLabel(
                app,
                text       = f"Volume : {int(setting['volume'])} %",
                font       = ("Copperplate Gothic Bold", int(LY * 0.028), "bold"),
                text_color = "#FFFFFF",
                fg_color   = "#0a0a1a"
            )
            aff_vol.place(x=int(LX * 0.05), y=int(LY * 0.3))
            settings_overlay.append(aff_vol)
            def mod_vol(value):
                with open(fichier_setting, "r", encoding="utf-8") as jason: setting = json.load(jason)
                setting["volume"] = value
                with open(fichier_setting, "w", encoding="utf-8") as jason: json.dump(setting, jason, indent=4)
                aff_vol.configure(text=f"Volume : {int(value)}%")
            slider_vol = ctk.CTkSlider(
                app,
                from_       = 0,
                to          = 100,
                command     = mod_vol,
                width       = int(LX * 0.3),
                height      = int(LY * 0.03),
                bg_color    ="#0a0a1a",
            )
            slider_vol.set(setting["volume"])
            slider_vol.place(x=int(LX * 0.05), y=int(LY * 0.35))
            settings_overlay.append(slider_vol)
            def key_bind(commande, event):
                nonlocal setting
                key = event.keysym
                app.unbind("<Key>")
                with open(fichier_setting, "r", encoding="utf-8") as jason: setting = json.load(jason)
                if key in setting["keys"]:return
                else:
                    dic_tempo = {}
                    dic_tempo2= {}
                    for i, y in setting["keys"].items():
                        if i in ("Up", "Down", "Right", "Left"): continue
                        else:
                            dic_tempo[y] = str(i)
                    dic_tempo[commande] = key
                    for j, h in dic_tempo.items():
                        dic_tempo2[h] = j
                    for o, l in setting["default_keys"].items():
                        if o in ("Up", "Down", "Right", "Left"):
                            dic_tempo2[o] = l
                        else: continue
                    setting.pop("keys")
                    setting["keys"] = dic_tempo2
                    with open(fichier_setting, "w", encoding="utf-8") as jason: json.dump(setting, jason, indent=4)
                    with open(fichier_setting, "r", encoding="utf-8") as jason: setting = json.load(jason)
                    menu_setting(True)
            def reset_default():
                with open(fichier_setting, "r", encoding="utf-8") as jason: setting = json.load(jason)
                setting["keys"] = setting["default_keys"]
                with open(fichier_setting, "w", encoding="utf-8") as jason: json.dump(setting, jason, indent=4)
                with open(fichier_setting, "r", encoding="utf-8") as jason: setting = json.load(jason)
            e=LY*0.1; v = LX*0.45
            for i in setting["keys"]:
                if i in ("Up", "Down", "Right", "Left"): continue
                else:
                    lb1 = ctk.CTkLabel(
                        app,
                        text        = f"{setting["keys"][i]}",
                        font        = ("Copperplate Gothic Bold", int(LY*0.035), "bold"),
                        text_color  = "#FFFFFF",
                        fg_color    = "#0a0a1a",
                        anchor      = "center"
                    )
                    lb1.place(x=v, y=e)
                    settings_overlay.append(lb1)
                    lb2 = ctk.CTkLabel(
                        app,
                        text        = f"[{i}]",
                        font        = ("Copperplate Gothic Bold", int(LY*0.035), "bold"),
                        text_color  = "#FFFFFF",
                        fg_color    = "#0a0a1a",
                        anchor      = "center"
                    )
                    lb2.place(x=(v+LX*0.3), y=e)
                    settings_overlay.append(lb2)
                    bt1 = bouton(
                        app         = app,
                        text        = "Modifier",
                        command     = lambda i=i, : app.bind(
                            "<Key>",
                            lambda event,
                            cmd=setting["keys"][i]: key_bind(
                                cmd,
                                event
                            )
                        ),
                        font        = ("Copperplate Gothic Bold", LY*0.03, "bold")
                    ).place(v+LX*0.4, e-10)
                    settings_overlay.append(bt1)
                    e += LY*0.11
            settings_overlay.append(
                bouton(
                    app,
                    "reset",
                    lambda:(
                        reset_default(),
                        menu_setting(True)
                    ),
                    ("Copperplate Gothic Bold", int(LY*0.035), "bold")
                ).place(LX*0.05, LY*0.7)
            )
            settings_overlay.append(
                bouton(
                    app,
                    "back",
                    lambda: (
                        menu_setting(False),
                    ),
                    ("Ubuntu", int(LY*0.02), "bold"),
                    "#707070",
                    "#FF0000"
                ).place(LX*0.03, LY*0.9)
            )
        elif not actif:
            SCAPE = False
            if settings_overlay:
                for widget in settings_overlay:
                    try: widget.destroy()
                    except: pass
                settings_overlay = None
            app.bind("<Key>", action)
            app.bind("<KeyRelease>", relacher)
            return

    def save():
        nonlocal instance
        dossier_save = os.path.join(os.path.dirname(__file__), "Save")
        if len(os.listdir(dossier_save)) < 6:
            with open(os.path.join(dossier_save, f"{instance['name']}_{datetime.now().strftime('%d-%m-%Y_%Hh%M')}.json"), "w", encoding="utf-8") as jason:
                json.dump(instance, jason, indent=4)
            quit_to_title([popup("Game saved", 3000, "green")])
        else: popup("backup failed \n too many backup", 5000, "red")
    
    def quit_to_title(exp=[]):
        for proj in projectiles_actifs:
            proj.actif = False
        projectiles_actifs.clear()
        app.unbind("<Key>")
        app.unbind("<KeyRelease>")
        global PL, ED, SCAPE, ITEM_SELECT, hud_canvas
        global touch_push, mobs_img, obj_img, MOBS, OBJ, ITEMS, direc
        global pause_overlay, settings_overlay
        PL              = 0
        ED              = None
        SCAPE           = False
        ITEM_SELECT     = 1
        hud_canvas      = None
        touch_push      = set()
        mobs_img        = []
        obj_img         = []
        MOBS            = {}
        OBJ             = {}
        ITEMS           = []
        direc           = "S"
        pause_overlay   = None
        settings_overlay= None
        clear(exp)
        if on_quit:
            on_quit()

    def action(event):
        nonlocal position_actuel
        global SCAPE
        touche = event.keysym
        if touche in touch_push:
            return
        touch_push.add(touche)
        if touche in setting["keys"]:
            if setting["keys"][touche] in ["forward", "backward", "right", "left"]:
                direction = setting["keys"][touche]
                NEW_POS = [position_actuel[0], position_actuel[1]]

                if direction == "forward":
                    if position_actuel == [0, 5] or position_actuel == [0, 6]:
                        change_frame(direction)
                        return
                    else:NEW_POS[0] -= 1

                elif direction == "backward":
                    if position_actuel == [NB_LI-1, 5] or position_actuel == [NB_LI-1, 6]:
                        change_frame(direction)
                        return
                    else:NEW_POS[0] += 1

                elif direction == "right":
                    if position_actuel == [3, NB_COL-1]:
                        change_frame(direction)
                        return
                    else:NEW_POS[1] += 1

                elif direction == "left":
                    if position_actuel == [3, 0]:
                        change_frame(direction)
                        return
                    else:NEW_POS[1] -= 1

                if accessible(NEW_POS[0], NEW_POS[1]):
                    position_actuel = [NEW_POS[0], NEW_POS[1]]
                move(position_actuel ,direction)
            elif setting["keys"][touche] in ["Attack", "defense"]:
                if setting["keys"][touche] == "Attack":
                    attaque(position_actuel, direc, instance["inventair"][ITEM_SELECT-1])
                    actualiser_mobs()
                elif setting["keys"][touche] == "defense":
                    return
            elif setting["keys"][touche] in ["Select_next_item", "Select_previous_item"]:
                if setting["keys"][touche] == "Select_next_item":
                    swipe("right")
                elif setting["keys"][touche] == "Select_previous_item":
                    swipe("left")
        elif touche == "Escape":
            SCAPE = not SCAPE
            if SCAPE:
                menu_escape(SCAPE)
            else:
                menu_escape(SCAPE)

    def relacher(event):
        touch_push.discard(event.keysym)

    def cal_epic():
        global epic 
        alpha   = 0.1
        beta    = 0.5
        gamma   = 0.4
        nv      = lv
        nvm     = 9
        hp      = instance["heart"]
        hpm     = instance["max_heart"]
        nbm = 0
        for mob in MOBS:
            if MOBS[mob].map_pos == position_actuel:
                nbm += 1
            else: continue
        nbmm    = int(0.17*((lv-1)**2)+2)
        epik    = alpha*(nv/nvm)+beta*(1-(hp/hpm))+gamma*(nbm/nbmm)
        if epik < 0.33: epique = 1
        elif 0.33 <= epik <= 0.66: epique = 2
        else: epique = 3
        if epique != epic:
            code_audio.game_mode(app, epique)
            epic = epique
            print(f"nouveau epic {int(epique)}")
        print("epic app")
        app.after(10000, lambda: cal_epic())
        

    app.bind("<Key>", action)
    app.bind("<KeyRelease>", relacher)
    code_audio.jouer_son(playlist=playlist_menu, volume=int(setting["volume"]))
    cal_epic()
    actualise_zero()
    initialisation_img()
    actualiser_frame()
    move(position_actuel, direction="right")

if __name__ == "__main__":
    import ctypes
    try:
        ctypes.windll.user32.SetProcessDPIAware()
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except:
        pass
    app = ctk.CTk()
    app.title("DeadLine Panic")
    app.geometry("1600x900")
    app.state("zoomed")
    app.aspect(16, 9, 16, 9)
    ctk.deactivate_automatic_dpi_awareness()
    ctk.set_appearance_mode("dark")

    # niv = int(input("select lv > "))

    start(app, 1)
    app.mainloop()