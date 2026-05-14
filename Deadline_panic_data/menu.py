import customtkinter as ctk
import os
import json
import level_selection
import random
import ctypes
from PIL import Image
from datetime import datetime
import code_audio
import sound_manager
# ========== Correction DPI ==========
try:
    ctypes.windll.user32.SetProcessDPIAware() 
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except:
    pass
# ========== Configuration ==========
dossier = os.path.dirname(__file__)
# ========== Configuration customtkinter==========

def menu(app):

    LX                      = app.winfo_width()
    LY                      = app.winfo_height()
    ZEROX                   = LX//2
    ZEROY                   = LY//2
    fichier_preset          = os.path.join(dossier, "preset_placement.json")
    with open(fichier_preset, "r", encoding="utf-8") as jason: preset = json.load(jason)
    playlist_menu           = preset["playlists"]["playlist_menu"]
    playlist_epic1          = preset["playlists"]["playlist_epic"]["playlist_epic1"]
    playlist_epic2          = preset["playlists"]["playlist_epic"]["playlist_epic2"]
    playlist_epic3          = preset["playlists"]["playlist_epic"]["playlist_epic3"]
    fich = os.path.join(dossier, "settings.json")
    with open(fich, "r", encoding="utf-8") as jason : setting = json.load(jason)
    code_audio.jouer_son(playlist=playlist_menu, loop=True, volume=int(setting["volume"]))

    def clear():
        for widget in app.winfo_children():
            widget.destroy()

    class texte: 
        def __init__(self, text, font=("Copperplate Gothic Bold", LY*0.05, "bold"), parent=None):
            ZERO()
            self.widget = ctk.CTkLabel(
                parent if parent else app,
                text            = text,
                font            = font,
                text_color      = "#FFFFFF",
                fg_color        = "transparent",
                anchor          = "center"
            )
        def configure(self, value):
            self.widget.configure(text=value)
        def place(self, x, y):
            self.widget.place(x=x, y=y)
            return self
        def relplace(self, x, y):
            self.widget.place(relx=x, rely=y)
            return self
        def pack(self, padx, pady, anchor, side=None, expand=False):
            self.widget.pack(padx=padx, pady=pady, anchor=anchor, side=side, expand=expand)
            return self
        def infox(self):
            return self.widget.winfo_width()
        def infoy(self):
            return self.widget.winfo_height()

    class image:
        def __init__(self, img, size=(20, 20), parent=None):
            ZERO()
            self.image = ctk.CTkImage(
                dark_image=Image.open(img),
                size=size
            )
            self.widget = ctk.CTkLabel(
                parent if parent else app,
                fg_color="transparent",
                image= self.image,
                text="",
                anchor="center"
            )
        def place(self, x, y):
            self.widget.place(x=x, y=y)
            return self
        def pack(self, padx, pady, anchor, side=None):
            self.widget.pack(
            padx=padx,
            pady=pady,
            anchor=anchor,
            side=side
            )

    class bouton: 
        def __init__(self, text, command, font=("Copperplate Gothic Bold", LY*0.03, "bold"),
                col_enter="white" , col_out="#FFD700", parent=None
            ):
            ZERO()
            self.widget = ctk.CTkButton(
                parent if parent else app,
                text                = text,
                font                = font,
                width               = 200,
                height              = 50,
                fg_color            = "transparent",
                hover_color         = "#3a3a3a",
                text_color          = "white",
                text_color_disabled = "gray",
                command             = command,
                border_width        = 0
            )
            self.widget.bind("<Enter>", lambda e: self.widget.configure(text_color=col_out))
            self.widget.bind("<Leave>", lambda e: self.widget.configure(text_color=col_enter))
        def place(self, x , y):
            self.widget.place(x=x, y=y)
            return self
        def pack(self, padx, pady, anchor, side=None):
            self.widget.pack(padx=padx, pady=pady, anchor=anchor, side=side)
            return self
        def cacher(self):
            self.widget.place_forget()
        def place_center(self,x=None, y=None):
            w = self.widget.cget("width")
            h = self.widget.cget("height")
            self.widget.place(
                x=x - w//2,
                y=y - h//2,
                anchor="center"
            )
            return self

    class choice_buton:
        def __init__(self, text, value, variable, font=("Copperplate Gothic Bold", int(LY*0.035), "bold"),
                parent=None
            ):
            ZERO()
            self.widget = ctk.CTkRadioButton(
                parent if parent else app,
                text=text,
                font=font,
                variable=variable,
                value=value
            )
        def pack(self, padx, pady, anchor, side=None):
            self.widget.pack(padx=padx, pady=pady, anchor=anchor, side=side)
            return self
        def place(self, x , y):
            self.widget.place(x=x, y=y)

    class enter:
        def __init__(self, text, parent=None):
            ZERO()
            self.widget = ctk.CTkEntry(
                parent if parent else app,
                placeholder_text= text,
                width=LX*0.15,
                height=LY*0.05,
                font=("Copperplate Gothic Bold", int(LY*0.02), "bold")
            )
        def place(self, x, y):
            self.widget.place(x=x, y=y)
            return self
        def cacher(self):
            self.widget.place_forget()
        def get(self):
            return self.widget.get()
        def pack(self, padx=0, pady=0, anchor="center", side=None):  # ← ajoute méthode pack
            self.widget.pack(padx=padx, pady=pady, anchor=anchor, side=side)
            return self   
        
    class slider:
        def __init__(self, from_, to, commande):
            ZERO()
            self.widget = ctk.CTkSlider(
                app,
                from_ = from_,
                to = to,
                command=commande,
                width=LX*0.2,
                height=LY*0.02
            )
        def sett(self, value):
            self.widget.set(value)
        def place(self, x, y):
            self.widget.place(x=x, y=y)
            return self
        def pack(self, padx, pady, anchor):
            self.widget.pack(padx=padx, pady=pady, anchor=anchor)

    class frame_line:
        def __init__(self, pady=5):
            ZERO()
            self.widget = ctk.CTkFrame(
                app,
                fg_color="transparent"
            )
            self.widget.pack(pady=pady, anchor="center")
        def contenu(self):
            return self.widget

    def ZERO():
        nonlocal LX, LY, ZEROX, ZEROY
        LX = app.winfo_width()
        LY = app.winfo_height()
        ZEROX = LX//2
        ZEROY = LY//2

    def menu_main():
        ZERO()
        image(img=os.path.join(os.path.join(dossier, "Texture\\frames\\fond.png")), size=(LX, LY),).place(0,0)
        texte("DeadLine  Panic").place((LX//20)*1, (LY//10)*1)
        bouton("New Game",  lambda:(clear(), menu_new_game()))  .place((LX//20)*1, (LY//10)*3)
        bouton("Load Game", lambda:(clear(), menu_load_game())) .place((LX//20)*1, (LY//10)*5)
        bouton("Setting",   lambda:(clear(), menu_setting()))   .place((LX//20)*1, (LY//10)*7)
        bouton("Leave",     app.destroy, ("Ubuntu", int(LY*0.02), "bold"), "#707070", "#FF0000").place((LX//20)*1, (LY//10)*9)
        code_audio.afficher(app, pos=[int(LX*0.75), int(LY*0.80)], perce=0.1, bg_col="#242424")

    def menu_new_game():
        def register():
            parameter = {
                "character"     : 2,
                "name"          : "iD10T",
                "seed"          : 1234567890,
                "difficulty"    : 1,
                "max_heart"     : 6,
                "heart"         : 6,
                "max_abso"      : 2,
                "abso"          : 0,
                "speed"         : 10,
                "defense"       : 0,
                "attaque"       : 0,
                "inventair"     : [],
                "lv"            : 1,
                "epic_lv"       : 0
            }
            with open(os.path.join(dossier, "preset_placement.json"), "r") as f : preset_placement = json.load(f)
            if choix_character.get() != 0 :
                parameter["character"]      = choix_character.get()
                parameter["max_heart"]      = preset_placement["preset_characters"][str(choix_character.get())]["max_heart"]
                parameter["heart"]          = preset_placement["preset_characters"][str(choix_character.get())]["max_heart"]
                parameter["max_abso"]       = preset_placement["preset_characters"][str(choix_character.get())]["max_abso"]
                parameter["speed"]          = preset_placement["preset_characters"][str(choix_character.get())]["speed"]
                parameter["defense"]        = preset_placement["preset_characters"][str(choix_character.get())]["defense"]
                parameter["attaque"]        = preset_placement["preset_characters"][str(choix_character.get())]["attaque"]
            if   choix_weapon.get() == 1    : parameter["inventair"].append("Latte")
            elif choix_weapon.get() == 2    : parameter["inventair"].append("Book")
            elif choix_weapon.get() == 3    : parameter["inventair"].append("Pen")
            if enter_name.get() != ""       : parameter["name"] = enter_name.get()
            if RAN["ran"]:
                seed = ""
                for i in range(10)          : seed += str(random.randint(0, 9))
                parameter["seed"] = int(seed)
            else                            : parameter["seed"] = int(enter_seed.get())
            if choix_dificult != 0          : parameter["difficulty"] = choix_dificult.get()
            dossier_save = os.path.join(dossier, "Save")
            with open(os.path.join(dossier_save, "instance.json"), "w") as f : json.dump(parameter, f, indent=4)
        ZERO()
        TAILLE_IM = LY*0.1
        dossier_image = os.path.join(dossier, "Texture\\menu")
        texte("choix du personnage", ("Copperplate Gothic Bold", int(LY*0.05), "bold")).pack(None, int(LY*0.02), "center")
        ligne_img_perso = frame_line(pady=LY*0.002)
        f1 = ligne_img_perso.contenu()
        image(os.path.join(dossier_image, "1.png"), (TAILLE_IM, TAILLE_IM), parent=f1).pack(int(LX*0.05), 5, "center", "left")
        image(os.path.join(dossier_image, "2.png"), (TAILLE_IM, TAILLE_IM), parent=f1).pack(int(LX*0.05), 5, "center", "left")
        image(os.path.join(dossier_image, "3.png"), (TAILLE_IM, TAILLE_IM), parent=f1).pack(int(LX*0.05), 5, "center", "left")
        choix_character = ctk.IntVar(value=0)
        ligne_radio_perso = frame_line(pady=LY*0.002)
        f2 = ligne_radio_perso.contenu()
        choice_buton("Speed",     1, choix_character, parent=f2).pack(int(LX*0.05), 5, "center", "left")
        choice_buton("Classique", 2, choix_character, parent=f2).pack(int(LX*0.05), 5, "center", "left")
        choice_buton("Heart",     3, choix_character, parent=f2).pack(int(LX*0.05), 5, "center", "left")
        texte("choix de l'arme",("Copperplate Gothic Bold", int(LY*0.05), "bold")).pack(None, int(LY*0.02), "center")
        ligne_img_arm = frame_line(pady=LY*0.002)
        f3 = ligne_img_arm.contenu()
        image(os.path.join(dossier_image, "latte.png"), (TAILLE_IM, TAILLE_IM), parent=f3).pack(int(LX*0.05), 5, "center", side="left")
        image(os.path.join(dossier_image, "book.png"),  (TAILLE_IM, TAILLE_IM), parent=f3).pack(int(LX*0.05), 5, "center", side="left")
        image(os.path.join(dossier_image, "pen.png"),   (TAILLE_IM, TAILLE_IM), parent=f3).pack(int(LX*0.05), 5, "center", side="left")
        choix_weapon = ctk.IntVar(value=0)
        ligne_radio_arm = frame_line(pady=LY*0.002)
        f4 = ligne_radio_arm.contenu()
        choice_buton("Latte", 1, choix_weapon, parent=f4).pack(int(LX*0.05), 5, "center", side="left")
        choice_buton("Farde", 2, choix_weapon, parent=f4).pack(int(LX*0.05), 5, "center", side="left")
        choice_buton("Bic",   3, choix_weapon, parent=f4).pack(int(LX*0.05), 5, "center", side="left")
        texte("choix de la dificulter",("Copperplate Gothic Bold", int(LY*0.05), "bold")).pack(None, int(LY*0.02), "center")
        ligne_img_difi = frame_line(pady=LY*0.002)
        f5 = ligne_img_difi.contenu()
        image(os.path.join(dossier_image, "dificulty_1.png"),   (TAILLE_IM, TAILLE_IM), parent=f5).pack(int(LX*0.065), 5, "center", side="left")
        image(os.path.join(dossier_image, "dificulty_2.png"),   (TAILLE_IM, TAILLE_IM), parent=f5).pack(int(LX*0.065), 5, "center", side="left")
        image(os.path.join(dossier_image, "dificulty_3.png"),   (TAILLE_IM, TAILLE_IM), parent=f5).pack(int(LX*0.065), 5, "center", side="left")
        image(os.path.join(dossier_image, "dificulty_4.png"),   (TAILLE_IM, TAILLE_IM), parent=f5).pack(int(LX*0.065), 5, "center", side="left")
        image(os.path.join(dossier_image, "dificulty_5.png"),   (TAILLE_IM, TAILLE_IM), parent=f5).pack(int(LX*0.065), 5, "center", side="left")
        choix_dificult = ctk.IntVar(value=0)
        ligne_radio_dificulter = frame_line(pady=LY*0.002)
        f6 = ligne_radio_dificulter.contenu()
        choice_buton("Normal", 1, choix_dificult, parent=f6).pack(int(LX*0.04), 5, "center", side="left")
        choice_buton("Difficile", 2, choix_dificult, parent=f6).pack(int(LX*0.04), 5, "center", side="left")
        choice_buton("Expert", 3, choix_dificult, parent=f6).pack(int(LX*0.04), 5, "center", side="left")
        choice_buton("Calvaire", 4, choix_dificult, parent=f6).pack(int(LX*0.04), 5, "center", side="left")
        choice_buton("Tourment", 5, choix_dificult, parent=f6).pack(int(LX*0.04), 5, "center", side="left")
        ligne_nom = frame_line(pady=int(LY * 0.05))
        f7 = ligne_nom.contenu()
        enter_name = enter("Votre nom...", parent=f7)
        enter_name.widget.pack(side="left", padx=int(LX*0.02))
        RAN = {"ran" : True}
        enter_seed = enter("Seed", parent=f7)
        bouton_seed_ran = bouton(
            "Random seed",
            lambda:(
                enter_seed.widget.pack_forget(),
                RAN.update({"ran" : True}),
                bouton_seed_ran.widget.pack_forget(),
                bouton_seed_def.widget.pack(side="left", padx=10)
            ),
            ("Copperplate Gothic Bold", LY*0.03, "bold"),
            parent=f7
        )
        bouton_seed_def = bouton(
            "définir la seed",
            lambda:(
                enter_seed.widget.pack(side="left", padx=10),
                RAN.update({"ran" : False}),
                bouton_seed_def.widget.pack_forget(),
                bouton_seed_ran.widget.pack(side="left", padx=10)
            ),
            ("Copperplate Gothic Bold", LY*0.03, "bold"),
            parent=f7
        )
        bouton_seed_def.widget.pack(side="left", padx=10)
        ligne_nav = frame_line(pady=int(LY * 0.002))
        f8 = ligne_nav.contenu()
        bouton("back",  lambda:(clear(), menu_main()), ("Ubuntu", LY*0.02, "bold"), "#707070", "#FF0000", parent=f8).pack(int(LX * 0.2), 5, "center", side="left")
        bouton("Start", lambda:(register(), clear(), level_selection.lv_select_screen(app)), parent=f8).pack(int(LX * 0.2), 5, "center", side="left")
        
    def menu_load_game():
        ZERO()
        texte("Choix de la save").pack(None, LY*0.07, "center")
        dossier_save = os.path.join(dossier, "Save")
        list_save = os.listdir(dossier_save)
        def charge_save(source):
            with open(source, "r") as f : contenu = json.load(f)
            with open(os.path.join(dossier_save, "instance.json"), "w") as f : json.dump(contenu, f, indent=4)
        def charge_deleted(source):
            os.remove(source)
        def valid_charge(fich):
            bouton("valide", lambda:(charge_save(fich), clear(), level_selection.lv_select_screen(app))).place(LX*0.8, LY*0.9)
        def delete_charge(fich):
            bouton("delete", lambda: (charge_deleted(fich), clear(), menu_load_game())).place_center(LX*0.5, LY*0.9)

        dic_save = {}
        tot = 0
        for i in list_save:
            if i == "instance.json": continue
            if i.endswith(".json"):
                fich = os.path.join(dossier_save, i)
                stats = os.stat(fich)
                with open(fich, "r", encoding="utf-8") as jason:
                    data = json.load(jason)
                date = datetime.fromtimestamp(stats.st_mtime).strftime("%d/%m/%Y %H:%M")
                dic_save[i] = bouton(
                    f"{data["name"]} - {date}",
                    lambda fich=fich:(
                        valid_charge(fich),
                        delete_charge(fich)
                    )
                ).pack(None, LY*0.05, "center")
            else:
                continue
            tot += 1
            if tot >= 5:
                break
        bouton("back", lambda:(clear(), menu_main()), ("Ubuntu", LY*0.02, "bold"), "#707070", "#FF0000").place(LX*0.1, LY*0.9)

    def menu_setting():
        ZERO()
        texte("Setting").place(LX*0.05, LY*0.11)
        fich = os.path.join(dossier, "settings.json")
        with open(fich, "r", encoding="utf-8") as jason : setting = json.load(jason)
        aff_vol = texte(f"Volume : {int(setting["volume"])}%", ("Copperplate Gothic Bold", int(LY*0.03), "bold")).place(LX*0.05, LY*0.3)
        def mod_vol(value):
            with open(fich, "r", encoding="utf-8") as jason: setting = json.load(jason)
            setting["volume"] = value
            code_audio.set_vol(int(value))
            with open(fich, "w", encoding="utf-8") as jason: json.dump(setting, jason, indent=4)
            aff_vol.configure(f"Volume : {int(value)}%")
        slide_volume = slider(0, 100, mod_vol).place(LX*0.05, LY*0.35)
        slide_volume.sett(setting["volume"])
        bouton("Credit", lambda:(clear(), Credit_screen())).place(LX*0.05, LY*0.5)
        def key_bind(commande, event):
            key = event.keysym
            app.unbind("<Key>")
            with open(fich, "r", encoding="utf-8") as jason: setting = json.load(jason)
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
                with open(fich, "w", encoding="utf-8") as jason: json.dump(setting, jason, indent=4)
                clear()
                menu_setting()

        def reset_default():
            with open(fich, "r", encoding="utf-8") as jason: setting = json.load(jason)
            setting["keys"] = setting["default_keys"]
            with open(fich, "w", encoding="utf-8") as jason: json.dump(setting, jason, indent=4)
        e=LY*0.1; v = LX*0.45
        for i in setting["keys"]:
            if i in ("Up", "Down", "Right", "Left"): continue
            else:
                texte(f"{setting["keys"][i]}", ("Copperplate Gothic Bold", int(LY*0.035), "bold")).place(v, e)
                texte(f"[{i}]", ("Copperplate Gothic Bold", int(LY*0.035), "bold")).place(v+LX*0.3, e)
                bouton("Modifier",  lambda i=i, : app.bind("<Key>", lambda event, cmd=setting["keys"][i]: key_bind(cmd, event))).place(v+LX*0.4, e-10)
                e += LY*0.11
        bouton("reset", lambda:(reset_default(), clear(), menu_setting())).place(LX*0.05, LY*0.7)
        bouton("back", lambda:(clear(), menu_main()), ("Ubuntu", LY*0.02, "bold"), "#707070", "#FF0000").place(LX*0.03, LY*0.9)

    def Credit_screen():
        Titre_Credit = texte("Credit").pack(None, 20, "center")
        credit = texte("voici les credit", ("Copperplate Gothic Bold", 24, "bold")).pack(None, 40, "center")
        bouton_back = bouton("back", lambda:(clear(), menu_setting()), ("Ubuntu", 16, "bold"), "#707070", "#FF0000").place(20, 750)

    menu_main()
    app.mainloop()

if __name__ == "__main__":
    app = ctk.CTk()
    app.title("DeadLine Panic")
    app.geometry("960x540")         # taille de la fenêtre
    app.state("zoomed")             # plein écran maximisé
    app.aspect(16, 9, 16, 9)        # force le ratio 16:9
    ctk.deactivate_automatic_dpi_awareness()
    ctk.set_appearance_mode("dark") # couleur
    menu(app)
