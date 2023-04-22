import webview
import pygame
from entity import Entity
from settings import *

class Terminal(Entity):
    def __init__(self, x, y, groupes, id=-1, locked=False):
        """Objet Terminal interactif par le joueur, créé une instance de Browser si interaction.

        Args:
            x (int): position x
            y (int): position y
            groupes (list): liste de pygame.sprite.Group auxquels ajouter le terminal
            id (int, optional): id du terminal. Defaults to -1.
            locked (bool, optional): True si le terminal est bloqué par défaut. Defaults to False.
        """
        self.image = load_terminal_img()
        super().__init__(x, y, self.image, groupes)
        self.id = int(str(id).strip())
        self.html = load_html(self.id) #TODO à compléter/activer lors de l'implémentation des sites
        self.surface = pygame.Rect(self.x, self.y+CASE_SIZE,CASE_SIZE*2,32)
        self.locked = locked
        self.using = False
        self.basey = self.surface.bottom

    def handle(self,player,surface, offset, settings):
        """Gère l'affichage des en-tête d'aide au joueur

        Args:
            player (player object): objet du joueur
            surface (Rect): rectangle de position du terminal
            offset (Camera.offset): vector2 d'offset de la caméra
            settings (dict): dictionnaire des paramètres pour les touches d'intéraction 
        """
        if player.check_distance_to(self.surface.midbottom, interact_distance) and self.surface.y < player.y:
            self.show_indicator(surface, offset, settings)

    def interact(self):
        """Interaction du joueur sur le terminal, créé l'instance Browser afin de proposer le quiz HTML au joueur

        Returns:
            bool: True si le joueur a réussi le quiz
        """
        if not self.locked:
            self.using = True
            browser = Browser(self.html,"TERMINAL")
            browser.show_browser()
            self.using = False
            if browser.succeded:
                return True, self.id
            else:
                return False, self.id
            
    def unlock(self):
        """Déverrouille le terminal
        """
        self.locked=False
    
    def lock(self):
        """Verrouille le terminal
        """
        self.locked = True
            
    def show_indicator(self,surface, offset, settings):
        """Affiche l'indicateur d'aide au joueur

        Args:
            surface (Rect): rectangle de position du terminal
            offset (Camera.offset): vector2 d'offset de la caméra
            settings (dict): dictionnaire des paramètres pour les touches d'intéraction 
        """
        if self.locked:
            surface.blit(font2.render("[Terminal verrouillé]",1,"white"), (self.x + self.surface.width + 5 - offset.x, self.y - 5 + self.surface.height - offset.y))
        else:
            surface.blit(font2.render(f"[{pygame.key.name(int(settings['k_interact'])).upper()}] pour interagir",1,"white"), (self.x - offset.x, self.y +10 + self.image.get_height() - offset.y))

class Browser:
    def __init__(self, html, title) -> None:
        """Objet Browser à l’intérieur d’un terminal, ouvre une fenêtre web via librairie pywebview

        Args:
            html (str): code html à passer dans la fenêtre pywebview
            title (str): titre de la fenêtre
        """
        self.api = Api()
        self.html = html
        self.title = title
        self.window = None
        self.succeded = False

    def show_browser(self):
        """Créé la fenêtre et l'affiche à l'écran. Code python arrêté dans cette fonction tant que la fenêtre n'est pas refermée
        """
        self.window = webview.create_window(self.title, html=self.html, resizable=False, fullscreen=True, js_api=self.api, background_color="#003300")
        self.api.set_window(self.window)
        webview.start()  
        if self.api.succeded:
            self.succeded = True     
    

class Api:

    def __init__(self):
        """Classe API permettant d'intéragir avec le code Javascript de la fenêtre pywebview. Voir documentation de la librairie pour plus de détails
        """
        self._window = None
        self.succeded =False

    def set_window(self, window):
        self._window = window

    def close_window(self):
        try:
            self._window.destroy()
        except KeyError:
            pass # erreur de la fonction .destroy() courante et non résolue à ce jour


    def completed(self):
        self.succeded = True
        self.close_window()

    def play_key_sound(self):
        # joue son clavier
        pygame.mixer.music.load(os.path.join(music_folder, "misc/key1_press.wav"))
        pygame.mixer.music.play()
        pass
