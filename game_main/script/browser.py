import webview
import pygame
from entity import Entity
from settings import *

class Terminal(Entity):
    def __init__(self, x, y, groupes, id=-1, locked=False):
        self.image = load_terminal_img()
        super().__init__(x, y, self.image, groupes)
        self.id = id
        #self.html = load_html(self.id) #TODO à compléter/activer lors de l'implémentation des sites
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
            browser = Browser("google.com","TERMINAL")
            browser.show_browser()
            self.using = False
            if browser.succeded:
                print("YOUHOU")
                return True, self.id
            else:
                return False, self.id
            

            
    def show_indicator(self,surface, offset, settings):
        if self.locked:
            surface.blit(font2.render("[Terminal verrouillé]",1,"white"), (self.x + self.surface.width + 5 - offset.x, self.y - 5 + self.surface.height - offset.y))
        else:
            surface.blit(font2.render(f"[{pygame.key.name(int(settings['k_interact'])).upper()}] pour interagir",1,"white"), (self.x - offset.x, self.y +10 + self.image.get_height() - offset.y))

class Browser:
    def __init__(self, html, title) -> None:
        self.html = html
        self.title = title
        self.window = None
        self.succeded = False

    def show_browser(self):
        self.window = webview.create_window(self.title, html=self.html, fullscreen=True, js_api=self)
        
        webview.start()       
    
    def close_window(self):
        self.window.destroy()

    def terminal_completed(self):
        # épreuve réussie 
        pass

    def plau_key_sound(self):
        # joue son clavier
        pass

    def connexion_reussie(self):
        # terminal 1 : réussie
        pass

# appel de "pythonFunction" dans JS
# window.pywebview.api.pythonFunction("arg");
