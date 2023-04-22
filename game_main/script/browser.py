import webview
import pygame
from entity import Entity
from settings import *

class Terminal(Entity):
    def __init__(self, x, y, groupes, id=-1, locked=False):
        self.image = load_terminal_img()
        super().__init__(x, y, self.image, groupes)
        self.id = int(str(id).strip())
        self.html = load_html(self.id) #TODO à compléter/activer lors de l'implémentation des sites
        self.surface = pygame.Rect(self.x, self.y+CASE_SIZE,CASE_SIZE*2,32)
        self.locked = locked
        self.using = False
        self.basey = self.surface.bottom

    def handle(self,player,surface, offset, settings):
        if player.check_distance_to(self.surface.midbottom, interact_distance) and self.surface.y < player.y:
            self.show_indicator(surface, offset, settings)

    def interact(self):
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
        self.locked=False
    
    def lock(self):
        self.locked = True
            
    def show_indicator(self,surface, offset, settings):
        if self.locked:
            surface.blit(font2.render("[Terminal verrouillé]",1,"white"), (self.x + self.surface.width + 5 - offset.x, self.y - 5 + self.surface.height - offset.y))
        else:
            surface.blit(font2.render(f"[{pygame.key.name(int(settings['k_interact'])).upper()}] pour interagir",1,"white"), (self.x - offset.x, self.y +10 + self.image.get_height() - offset.y))

class Browser:
    def __init__(self, html, title) -> None:
        self.api = Api()
        self.html = html
        self.title = title
        self.window = None
        self.succeded = False

    def show_browser(self):
        self.window = webview.create_window(self.title, html=self.html, resizable=False, fullscreen=True, js_api=self.api, background_color="#003300")
        self.api.set_window(self.window)
        webview.start()  
        if self.api.succeded:
            self.succeded = True     
    

class Api:

    def __init__(self):
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
