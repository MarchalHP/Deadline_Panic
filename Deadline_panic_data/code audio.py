from customtkinter import *
from PIL import Image
import os
import random
from sound_manager import SoundManager
from PIL import Image, ImageTk
import tkinter as tk

"""fenêtres"""
app = CTk()
app.geometry("400x240")
app.update()


"""variables"""
sound_manager           = SoundManager()
son_actif               = True
dossier = os.path.dirname(__file__)
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
        btn_son.configure(image=img_pause)
        son_actif = False
    else:
        sound_manager.setvolume(70)
        btn_son.configure(image=img_play)
        son_actif = True

def btn_favoris():
    global favoris
    if son.get("file") in favoris:
        favoris.remove(son["file"])
        btn_fav.configure(image=img_pasfavoris)
    else:
        favoris.append(son["file"])
        btn_fav.configure(image=img_favoris)
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

def afficher(app):
    LX = app.winfo_width()
    LY = app.winfo_height()
    canvar = tk.Canvas(
        app,
        width               = LX,
        height              = LY,
        bg                  = "#ffffff",
        highlightthickness  = 0
    )
    canvar.place(x=0, y=0)
    VX = canvar.winfo_width(),
    VY = canvar.winfo_height(),
    bg_image = image(image_play, size=(VX, VY))
    canvar.create_image(
        VX//2,
        VY//2,
        anchor="center",
        image=bg_image
    )
    canvar._fond = bg_image
    # bg_label = CTkLabel(app, image=bg_image, text="")
    # bg_label.place(x=0, y=60)
    bg_label = canvar.create_image(
        int((VX//2)+VX*0.01),
        int((VY//2)+VY*0.01),
        anchor="nw",
        image=bg_image
    )
    # btn_son = CTkLabel(app, image=img_play, text="", fg_color="transparent", padx=0, pady=0)
    # btn_son.place(x=60, y=100)
    btn_son = canvar.create_image(
        int((VX//2)+VX*0.01),
        int((VY//2)+VY*0.01),
        anchor="nw",
        image=bg_image
    )

    img_play        = image(image_play,         size=(40, 40))
    img_pause       = image(image_pause,        size=(40, 40))
    img_favoris     = image(image_favoris,      size=(40, 40))
    img_pasfavoris  = image(image_pasfavoris,   size=(40, 40))



    
    """affichage"""
    

    
    btn_son.bind("<Button-1>", lambda e: btn_volume())

    btn_fav = CTkLabel(app, image=img_pasfavoris, text="")
    btn_fav.place(x=300, y=100)
    btn_fav.bind("<Button-1>", lambda e: btn_favoris())

    lcd_ecran = CTkLabel(app, text="",
                        font=CTkFont(family="Courier New", size=12),
                        fg_color="#5c8a3f",
                        bg_color="#5c8a3f",
                        text_color="black")
    lcd_ecran.place(x=148, y=109)

"""démarrage"""
print(os.getcwd())
defilement()
check_fin_musique()
"""sound_manager.set_on_end(next_song)
sound_manager.mediaplayer_onendreached = next_song"""
app.protocol("WM_DELETE_WINDOW", fermer_app)
# TESTS - à enlever après
app.after(5000, lambda: game_mode("epic1"))   # epic1 après 5 secondes
app.after(15000, lambda: game_mode("epic2"))  # epic2 après 15 secondes
app.after(25000, lambda: game_mode("epic3"))  # epic3 après 25 secondes
app.mainloop()