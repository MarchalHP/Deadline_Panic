import threading
import vlc
import logging
import os
import errno

class SoundManager:
    """SoundManager est basé sur vlc et permet de :
        - jouer des sons
        - jouer une musique de fond en boucle
       La musique de fond peut être mise en pause et la lecture peut être
       reprise
       
       Exemple :
           # Joue une musique en boucle à 80% de volume
           soundManager = SoundManager()
           soundManager.setvolume(80)
           soundManager.playmusic('./sounds/forest-lullaby.mp3', True)
       
       Avant d'utiliser SoundManager, assure toi d'avoir installé vlc :
           pip install python-vlc
       Pour plus d'informations :
           https://wiki.videolan.org/Python_bindings/"""
    def __init__(self):
        self.__players = []
        self.__eventManagers = []
        self.__musicPlayer = None
        self.__musicPath = ""
        self.__loop = False
        self.__eventMusicManager = None
    
    def mediaplayer_onendreached(self, event):
        if (__name__ == "__main__"):
            logging.info("Son terminé" + repr(event))
        if (self.__loop):
            self.playmusic(self.__musicPath, self.__loop)
            
    """def __mediaplayer_onendreached(self, event):
        if (__name__ == "__main__"):
            logging.info("Son terminé" + repr(event))
        if (self.__loop):
            self.playmusic(self.__musicPath, self.__loop)
        elif hasattr(self, '_SoundManager__on_end_callback'):
            self.__on_end_callback(event)
    
    def set_on_end(self, callback):
        Permet de définir une fonction appelée quand la musique se termine
        self.__on_end_callback = callback"""
     
    def __mediaplayer_onendreached(self, event):
        if (self.__loop):
            self.playmusic(self.__musicPath, self.__loop)
        elif hasattr(self, '_SoundManager__on_end_callback'):
            self.__app.after(0, lambda: self.__on_end_callback(event))
     
    def set_on_end(self, callback, app):
        self.__on_end_callback = callback
        self.__app = app
    
    def __create_vlc_player(self, sound_path):
        if not(os.path.isfile(sound_path)):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), sound_path)
        player = vlc.MediaPlayer()
        media = vlc.Media(sound_path)
        player.set_media(media)
        return player
    
    def __thread_play(self, sound_path):
        player = self.__create_vlc_player(sound_path)
        self.__players.append(player)
        # self.eventManagers.append(self.players[-1].event_manager())
        # self.eventManagers[-1].event_attach(vlc.EventType.MediaPlayerEndReached, self.mediaplayer_onendreached)
        self.__players[-1].play()
        
    def __thread_playmusic(self, sound_path):
        self.__musicPlayer = self.__create_vlc_player(sound_path)
        self.__eventMusicManager = self.__musicPlayer.event_manager()
        self.__eventMusicManager.event_attach(vlc.EventType.MediaPlayerEndReached, self.__mediaplayer_onendreached)
        self.__musicPlayer.play()
      
    def playsound(self, sound_path):
        """Joue un son, un bruitage une fois.
        @sound_path: Chemin du fichier son à jouer
        
        Exemple :
            soundManager = SoundManager()
            soundManager.playsound('sound.mp3')"""
        
        x = threading.Thread(target=self.__thread_play, args=(sound_path, ))
        x.start()
        
    def playmusic(self, sound_path, loop = False):
        """Joue une musique, une fois ou en boucle.
        @sound_path: Chemin du fichier son à jouer
        @loop: True si la musique doit être jouée en boucle. False par défaut
        
        Exemple :
            soundManager = SoundManager()
            soundManager.playmusic('music.mp3')"""
        self.__musicPath = sound_path
        self.__loop = loop
        x = threading.Thread(target=self.__thread_playmusic, args=(sound_path, ))
        x.start()
        
    def pausemusic(self):
        """Met la musique en pause.
        La méthode playmusic doit être appelée au préalable.
        
        Exemple :
            soundManager = SoundManager()
            soundManager.playmusic('music.mp3')
            soundManager.pausemusic()"""
        if self.__musicPlayer:
            self.__musicPlayer.set_pause(1)
        
    def resumemusic(self):
        """Reprend la lecture de la musique après pause (méthode pausemusic)
        
        Exemple :
            soundManager = SoundManager()
            soundManager.playmusic('music.mp3')
            soundManager.pausemusic()
            soundManager.resumemusic()"""
        if self.__musicPlayer:
            self.__musicPlayer.play()
    
    def stopmusic(self):
        """Arrête uniquement la musique et pas les autres sons
        
        Exemple :
            soundManager = SoundManager()
            soundManager.playmusic('music.mp3')
            soundManager.stopmusic()"""
        if self.__musicPlayer:
            self.__musicPlayer.stop()
    
    def getvolume(self):
        """Récupère le volume
        
        Exemple :
            soundManager = SoundManager()
            vol = soundManager.getvolume()"""
        vlc_instance = vlc.Instance()
        player = vlc_instance.media_player_new()
        return player.audio_get_volume() 
        
    def setvolume(self, volume = 100):
        """Indique le volume pour toutes les bandes sonores.
        @volume: Entier de 0 à 100
        
        Exemple :
            soundManager = SoundManager()
            soundManager.setvolume(30)"""
        vlc_instance = vlc.Instance()
        player = vlc_instance.media_player_new()
        player.audio_set_volume(volume) 
        
    def stop(self):
        """Arrête tous les sons et musique en cours.
        Doit être impérativement appelé avant la fermeture du programme
        
        Exemple :
            soundManager = SoundManager()
            soundManager.stop()"""
        for player in self.__players:
            player.stop()
        self.stopmusic()

    def is_playing(self):
        if self.__musicPlayer:
            return self.__musicPlayer.is_playing()
        return False
    
if (__name__ == "__main__"):
    pass
