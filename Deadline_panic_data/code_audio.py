from customtkinter import *
from PIL import Image
import os
import random
import ctypes
from sound_manager import SoundManager
from PIL import Image, ImageTk
import tkinter as tk
import json
try:
    ctypes.windll.user32.SetProcessDPIAware() 
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except:
    pass
"""variables"""
sound_manager           = SoundManager()
son_actif               = True
dossier                 = os.path.dirname(__file__)
fichier_preset          = os.path.join(dossier, "preset_placement.json")
image_bg                = os.path.join(dossier, "Texture\\mp3\\mp3.png")
image_play              = os.path.join(dossier, "Texture\\mp3\\play.png")
image_pause             = os.path.join(dossier, "Texture\\mp3\\pause.png")
image_favoris           = os.path.join(dossier, "Texture\\mp3\\fav.png")
image_pasfavoris        = os.path.join(dossier, "Texture\\mp3\\no_favoris.png")
chemin_playlists        = os.path.join(dossier, "Playlist\\muse")
chemin_bruitages        = os.path.join(dossier, "Playlist\\Bruitages")
with open(fichier_preset, "r", encoding="utf-8") as jason: preset = json.load(jason)
playlist_menu           = preset["playlists"]["playlist_menu"]
playlist_epic1          = preset["playlists"]["playlist_epic"]["playlist_epic1"]
playlist_epic2          = preset["playlists"]["playlist_epic"]["playlist_epic2"]
playlist_epic3          = preset["playlists"]["playlist_epic"]["playlist_epic3"]
playlist_bruitage       = preset["playlists"]["playlist_bruitage"]
affichage_lecture       = []
affichage_ecran         = ""
cpt_defilement          = 0 
current_playlist        = None
current_loop            = False
volume_actuel           = 70
transition              = False
favoris                 = []
son                     = {}
canvar                  = None
lcd_ecran               = None
parent                  = None



def charger_fichier():
    global dossier, fichier_preset, image_bg, image_play, image_pause, image_pause, image_favoris, image_pasfavoris, chemin_playlists, chemin_bruitages, playlist_menu, playlist_epic1, playlist_epic2, playlist_epic3
    dossier                 = os.path.dirname(__file__)
    fichier_preset          = os.path.join(dossier, "preset_placement.json")
    image_bg                = os.path.join(dossier, "Texture\\mp3\\mp3.png")
    image_play              = os.path.join(dossier, "Texture\\mp3\\play.png")
    image_pause             = os.path.join(dossier, "Texture\\mp3\\pause.png")
    image_favoris           = os.path.join(dossier, "Texture\\mp3\\fav.png")
    image_pasfavoris        = os.path.join(dossier, "Texture\\mp3\\no_favoris.png")

    chemin_playlists        = os.path.join(dossier, "Playlist\\muse")
    chemin_bruitages        = os.path.join(dossier, "Playlist\\Bruitages")
    
    with open(fichier_preset, "r", encoding="utf-8") as jason: preset = jason.load(jason)
    
    playlist_menu           = preset["playlists"]["playlist_menu"]
    playlist_epic1          = preset["playlists"]["playlist_epic"]["playlist_epic1"]
    playlist_epic2          = preset["playlists"]["playlist_epic"]["playlist_epic2"]
    playlist_epic3          = preset["playlists"]["playlist_epic"]["playlist_epic3"]


def image(chemin_img, size=(50, 50)):
    img_pil = Image.open(chemin_img).convert("RGBA").resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(img_pil)

def defilement(app):
    global cpt_defilement, lcd_ecran
    if not lcd_ecran: return
    try:
        if affichage_ecran:
            affichage = affichage_ecran[cpt_defilement:] + affichage_ecran[:cpt_defilement]
            lcd_ecran.configure(text=affichage[:14])
            cpt_defilement = (cpt_defilement + 1) % len(affichage_ecran)
        app.after(200, lambda: defilement(parent))
    except Exception:
        lcd_ecran = None
        return
    
def next_song(event=None):
    if current_playlist and not current_loop:
        change_music(current_playlist)
              
def change_music(app, playlist, volume=None):
    global volume_actuel, transition
    transition = True
    # print("volume actuel:", volume_actuel)  # ← voir ce qui se passe
    if volume_actuel > 0:
        volume_actuel = max(0, volume_actuel - 5)
        sound_manager.setvolume(volume_actuel)

        app.after(50, lambda: change_music(app, playlist, volume))
    else:
        # print("STOP ET NOUVELLE MUSIQUE")  # ← voir si on arrive ici
        sound_manager.stopmusic()
        app.after(200, lambda: jouer_son(playlist, False, volume))
        volume_actuel = volume
              
def jouer_son(playlist, loop=False, volume=50):
    global affichage_lecture, affichage_ecran, current_loop, current_playlist, son
    son = random.choice(playlist)
    transition=False
    
    current_playlist = playlist
    current_loop = loop
    cpt_defilement = 0
    
    sound_manager.setvolume(volume)
    sound_manager.playmusic(f"{chemin_playlists}\\{son["file"]}", loop)
    affichage_lecture = [son["titre"], son["artiste"]]
    affichage_ecran = ""
    for info in affichage_lecture:
        affichage_ecran += info + "-"

def set_vol(volume=50):
    sound_manager.setvolume(volume)

def check_fin_musique():
    if not sound_manager.is_playing() and current_playlist and not current_loop and not transition:
        jouer_son(current_playlist, False)
    app.after(1000, check_fin_musique)
        
def game_mode(app, mode):
    if mode == 0:
        jouer_son(playlist_menu, True,30)
    elif mode == 1:
        change_music(app, playlist_epic1, 40)
        app.after(500, lambda: sound_manager.setvolume(40))
    elif mode == 2:
        change_music(app, playlist_epic2, 60)
        app.after(500, lambda: sound_manager.setvolume(70))
    elif mode == 3:
        change_music(app, playlist_epic3, 80)
        app.after(500, lambda: sound_manager.setvolume(100))

def bruitage(nom):
    chemin = os.path.join(chemin_bruitages, nom)
    sound_manager.playsound(chemin)

def reset():
    global current_playlist, current_loop, affichage_ecran, affichage_lecture
    global cpt_defilement, transition, son, canvar, lcd_ecran, parent
    sound_manager.stop()
    current_playlist    = None
    current_loop        = False
    affichage_ecran     = ""
    affichage_lecture   = []
    cpt_defilement      = 0
    transition          = False
    son                 = {}
    canvar              = None
    lcd_ecran           = None
    parent              = None

def fermer_app():
    reset()

def fermer_app():
    sound_manager.stop()

def afficher(app, pos=[0, 0], perce=0.12, bg_col="#ffffff"):
    global canvar, btn_son, btn_fav, lcd_ecran, parent  # ← ICI en premier, avant tout

    app.update_idletasks()
    app.update()

    LX = app.winfo_width()
    LY = app.winfo_height()

    CY = int(LY * perce)
    CX = int(3.2 * CY)

    marge = 20
    if pos == [0, 0]:
        pos = [LX - CX - marge, LY - CY - marge]

    if canvar:
        canvar.destroy()

    canvar = tk.Canvas(
        app,
        width              = CX,
        height             = CY,
        bg                 = bg_col,
        highlightthickness = 0
    )
    canvar.place(x=pos[0], y=pos[1])
    app.update_idletasks()

    TAIL_SON = (int(CY * 0.75), int(CY * 0.75))
    TAIL_FAV = (int(CY * 0.28), int(CY * 0.28))

    SX = int(CX * 0.20)
    SY = int(CY * 0.59)

    FX = int(CX * 0.3)
    FY = int(CY * 0.8)

    LCX = int(CX * 0.38)
    LCY = int(CY * 0.4)
    TT  = int(CY * 0.12)
    TL  = int(CX * 0.3)

    bg_image = image(image_bg, size=(CX, CY))
    canvar.create_image(0, 0, anchor="nw", image=bg_image)
    canvar._fond = bg_image

    img_play = image(image_play, size=TAIL_SON)
    btn_son = canvar.create_image(SX, SY, anchor="center", image=img_play)
    canvar._img_play = img_play

    img_pasfavoris = image(image_pasfavoris, size=TAIL_FAV)
    btn_fav = canvar.create_image(FX, FY, anchor="center", image=img_pasfavoris)
    canvar._img_fav = img_pasfavoris

    lcd_ecran = CTkLabel(
        canvar,
        text       = "Aucune musique",
        font       = CTkFont(family="Courier New", size=TT),
        fg_color   = "#5c8a3f",
        text_color = "black",
        anchor     = "w",
        width      = TL
    )
    lcd_ecran.place(x=LCX, y=LCY)
    parent = app
    defilement(parent)

    def btn_volume():
        global son_actif  # ← global dans la sous-fonction
        if son_actif:
            sound_manager.setvolume(0)
            img_pause = image(image_pause, size=TAIL_SON)
            canvar.itemconfig(btn_son, image=img_pause)
            canvar._img_pause = img_pause
            son_actif = False
        else:
            sound_manager.setvolume(70)
            img_play_new = image(image_play, size=TAIL_SON)
            canvar.itemconfig(btn_son, image=img_play_new)
            canvar._img_play = img_play_new
            son_actif = True

    def btn_favoris():
        global favoris  # ← global dans la sous-fonction
        if son.get("file") in favoris:
            favoris.remove(son["file"])
            img_pf = image(image_pasfavoris, size=TAIL_FAV)
            canvar.itemconfig(btn_fav, image=img_pf)
            canvar._img_fav = img_pf
        else:
            if son.get("file"):
                favoris.append(son["file"])
            img_f = image(image_favoris, size=TAIL_FAV)
            canvar.itemconfig(btn_fav, image=img_f)
            canvar._img_favoris = img_f

    canvar.tag_bind(btn_son, "<Button-1>", lambda e: btn_volume())
    canvar.tag_bind(btn_fav, "<Button-1>", lambda e: btn_favoris())



if __name__ == "__main__":
    app = CTk()
    app.geometry("800x250")
    app.update()
    afficher(app, [400, 125])
    app.mainloop()

#     """démarrage"""
#     print(os.getcwd())
#     defilement()
#     check_fin_musique()
#     """sound_manager.set_on_end(next_song)
#     sound_manager.mediaplayer_onendreached = next_song"""
#     app.protocol("WM_DELETE_WINDOW", fermer_app)
# # TESTS - à enlever après
# app.after(5000, lambda: game_mode("epic1"))   # epic1 après 5 secondes
# app.after(15000, lambda: game_mode("epic2"))  # epic2 après 15 secondes
# app.after(25000, lambda: game_mode("epic3"))  # epic3 après 25 secondes
# app.mainloop()