from customtkinter import *
from PIL import Image
import os
import random
import ctypes
from sound_manager import SoundManager
from PIL import Image, ImageTk
import tkinter as tk
try:
    ctypes.windll.user32.SetProcessDPIAware() 
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except:
    pass
"""variables"""
sound_manager           = SoundManager()
son_actif               = True
dossier                 = os.path.dirname(__file__)
image_bg                = os.path.join(dossier, "Texture\\mp3\\mp3.png")
image_play              = os.path.join(dossier, "Texture\\mp3\\play.png")
image_pause             = os.path.join(dossier, "Texture\\mp3\\pause.png")
image_favoris           = os.path.join(dossier, "Texture\\mp3\\fav.png")
image_pasfavoris        = os.path.join(dossier, "Texture\\mp3\\no_favoris.png")
chemin_playlists        = os.path.join(dossier, "Playlist\\muse")
chemin_bruitages        = os.path.join(dossier, "Playlist\\Bruitages")
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


"""playlists"""
playlist_menu  = [{"file":chemin_playlists+"02 Ange Halliwell - test.mp3","titre":"Test","artiste":"Ange Halliwell"},
                  {"file":chemin_playlists+"18 Organ Tapes - KHUSHI.mp3", "titre":"Organ Tape", "artiste":"KUSHI"},
                  {"file":chemin_playlists+"an1ssa_midi_orchestral_rework_2k20_slowed_instrumental_version.mp3","titre":"an1ssa_midi_orchestral","artiste":"oOryxss"},
                  {"file":chemin_playlists+"Tenhi - Näkin Laulu [1997 version].mp3", "titre":"Näkin Laulu","artiste":"Tenhi"},
                  {"file":chemin_playlists+"Obsequiae - Sidhe.mp3","titre":"Sidhe","artiste":"Obsequiae"}
                  ]
playlist_epic1 = [{"file":chemin_playlists+"012-city-Arclite.mp3", "titre":"City", "artiste":"Arclite"},
                  {"file":chemin_playlists+"Snafu.mp3","titre":"_+ᐸ(ᐳ_ᐸ)ᐳ+_===**++++++++__[--_ᐳᐳᐳᐳᐳ]}}}", "artiste":"Snafu"},
                  {"file":chemin_playlists+"Lurk - Oklou.mp3","titre":"Lurk","artiste":"Oklou"}, 
                  {"file":chemin_playlists+"BC - ghost ghoul.mp3","titre":"BC","artiste":"ghost ghoul"}]
playlist_epic2 = [{"file":chemin_playlists+"Enya-Aniron_Tomorrows_Gone_Remix.mp3","titre":"Aniron","artiste":"Tomorrows Gone"},
                  {"file":chemin_playlists+"Mission-Amon Tobin.mp3","titre":"Mission","artiste":"Amon Tobin"},
                  {"file":chemin_playlists+"09 KABLAM - enlife repeats.mp3","titre":"enlife repeats","artiste":"KABLAM"},
                  ]
playlist_epic3 = [{"file":chemin_playlists+"Autumnal Pyre.mp3", "titre":"Automnial Pyre","artiste":"Obsequiae"}]

Playlist_bruitages = {"arme_1":chemin_bruitages+"arme.mp3",
                      "arme_fleche":chemin_bruitages+"arme_arrow.mp3",
                      "arme_epée":chemin_bruitages+"arme_sword.mp3",
                      "porte":chemin_bruitages+"Door.mp3",
                      "you_win":chemin_bruitages+"epic_win.mp3",
                      "game_over":chemin_bruitages+"game_over.mp3",
                      "new_game":chemin_bruitages+"new_game.mp3",
                      "new_objet":chemin_bruitages+"new_item.mp3",
                      "points_de_vie":chemin_bruitages+"points_de_vie.mp3"
}
                     

def charger_fichier():
    dossier = os.path.dirname(__file__)
    image_bg                = os.path.join(dossier, "Texture\\mp3\\mp3.png")
    image_play              = os.path.join(dossier, "Texture\\mp3\\play.png")
    image_pause             = os.path.join(dossier, "Texture\\mp3\\pause.png")
    image_favoris           = os.path.join(dossier, "Texture\\mp3\\fav.png")
    image_pasfavoris        = os.path.join(dossier, "Texture\\mp3\\no_favoris.png")

    chemin_playlists        = os.path.join(dossier, "Playlist\\muse")
    chemin_bruitages        = os.path.join(dossier, "Playlist\\Bruitages")

def image(chemin_img, size=(50, 50)):
    img_pil = Image.open(chemin_img).convert("RGBA").resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(img_pil)

def btn_volume():
    global son_actif
    if son_actif: 
        sound_manager.setvolume(0)
        img_pause       = image(image_pause,        size=(40, 40))
        canvar.itemconfig(btn_son, image=img_pause)
        son_actif = False
    else:
        sound_manager.setvolume(70)
        img_play        = image(image_play,         size=(VX, VY))
        canvar.itemconfig(btn_son, image=img_play)
        son_actif = True

def btn_favoris():
    global favoris
    if son.get("file") in favoris:
        favoris.remove(son["file"])
        img_pasfavoris  = image(image_pasfavoris,   size=(40, 40))
        canvar.itemconfig(btn_fav, image=img_pasfavoris)
    else:
        favoris.append(son["file"])
        img_favoris     = image(image_favoris,      size=(40, 40))
        canvar.itemconfig(btn_fav, image=img_favoris)
        print(favoris)

def defilement():
    global cpt_defilement
    if affichage_ecran:
        affichage = affichage_ecran[cpt_defilement:] + affichage_ecran[:cpt_defilement]
        lcd_ecran.configure(text=affichage[:18])
        cpt_defilement = (cpt_defilement + 1) % len(affichage_ecran)
    app.after(200, defilement)      
    
def next_song(event=None):
    if current_playlist and not current_loop:
        change_music(current_playlist)
              
def change_music(playlist, volume=None):
    global volume_actuel, transition
    transition = True
    print("volume actuel:", volume_actuel)  # ← voir ce qui se passe
    if volume_actuel > 0:
        volume_actuel = max(0, volume_actuel - 5)
        sound_manager.setvolume(volume_actuel)
        app.after(50, lambda: change_music(playlist, volume))
    else:
        print("STOP ET NOUVELLE MUSIQUE")  # ← voir si on arrive ici
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
    sound_manager.playmusic(son["file"], loop)
    affichage_lecture = [son["titre"], son["artiste"]]
    affichage_ecran = ""
    for info in affichage_lecture:
        affichage_ecran += info + "-"

def check_fin_musique():
    if not sound_manager.is_playing() and current_playlist and not current_loop and not transition:
        jouer_son(current_playlist, False)
    app.after(1000, check_fin_musique)
        
def game_mode(mode):
    if mode == "menu":
        jouer_son(playlist_menu, True,30)
    elif mode == "epic1":
        change_music(playlist_epic1, 40)
        app.after(500, lambda: sound_manager.setvolume(40))
    elif mode == "epic2":
        change_music(playlist_epic2, 60)
        app.after(500, lambda: sound_manager.setvolume(70))
    elif mode == "epic3":
        change_music(playlist_epic3, 80)
        app.after(500, lambda: sound_manager.setvolume(100))

def bruitage(nom):
    sound_manager.playsound(Playlist_bruitages[nom])
       
def fermer_app():
    sound_manager.stop()
    app.destroy()
    os._exit(0)

def afficher(app, pos=[0, 0], perce=0.5):
    global canvar, btn_son, btn_fav, lcd_ecran
    app.update_idletasks()
    app.update()
    CY = int(app.winfo_height()*perce)
    CX = int(3.2 * CY)
    if canvar:
        canvar.destroy()

    # Canvas
    canvar = tk.Canvas(
        app,
        width              = CX,
        height             = CY,
        bg                 = "#ffffff",
        highlightthickness = 0
    )
    canvar.place(x=pos[0], y=pos[1])
    app.update_idletasks()

    BX = int((canvar.winfo_width()  *0.5) + pos[0])
    BY = int((canvar.winfo_height() *0.5) + pos[1])

    SX = int(-(canvar.winfo_width()  *0.295) + pos[0])
    SY = int((canvar.winfo_height() *0.06) + pos[1])
    TAIL_SON = (int(canvar.winfo_height()*0.7), int(canvar.winfo_height()*0.7))

    FX = int((canvar.winfo_width()  *0.275) + pos[0])
    FY = int((canvar.winfo_height() *0.00) + pos[1])
    TAIL_FAV = (int(canvar.winfo_height()*0.2), int(canvar.winfo_height()*0.2))

    bg_image = image(image_bg, size=(CX, CY))
    canvar.create_image(
        0,
        0,
        anchor  = "nw",
        image   = bg_image
    )
    canvar._fond = bg_image
    img_play = image(image_play, size=TAIL_SON)
    btn_son = canvar.create_image(
        SX,
        SY,
        anchor="center",
        image=img_play
    )
    canvar._img_play = img_play
    canvar.tag_bind(btn_son, "<Button-1>", lambda e: btn_volume())
    img_pasfavoris = image(image_pasfavoris, size=TAIL_FAV)
    btn_fav = canvar.create_image(
        FX,
        FY,
        anchor="center",
        image=img_pasfavoris
    )
    canvar._img_fav = img_pasfavoris
    canvar.tag_bind(btn_fav, "<Button-1>", lambda e: btn_favoris())
    lcd_ecran = CTkLabel(
        app,
        text       = "Aucune musique",
        font       = CTkFont(family="Courier New", size=12),
        fg_color   = "#5c8a3f",
        text_color = "black",
        width      = 200
    )
    lcd_ecran.place(x=CX - 100, y=CY - 20)  # Centré


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