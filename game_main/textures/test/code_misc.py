import pygame
from settings import *
from ui import Button


class MainMenu:
    def __init__(self, status):
        self.status = status #possibles : hidden, main, settings, saves
        self.surfaces = []
        self.buttons = []
        self.bg = pygame.transform.scale(pygame.image.load("..\\textures\\ui\\menu_bg.png"), (WIDTH,HEIGHT)).convert()
        self.title = pygame.sprite.Sprite()
        self.title.image = title_font.render(GAME_TITLE, 1, 'white')
        self.title.rect = self.title.image.get_rect(topleft = ((WIDTH-self.title.image.get_width())//2, 20))
        self.keys_names_rendered = {}
        for name in settings_name.values():
            font = pygame.sprite.Sprite()
            font.image = font1.render(name,1,"white").convert_alpha()
            self.keys_names_rendered[name] = font

    def show(self, screen):
        """Affiche le menu principal en fonction de son état
        """
        screen.blit(self.bg,(0,0))
        for surface in self.surfaces:
            screen.blit(surface.image, surface.rect)

    def handle(self):

        if self.status == "hidden":
            self.surfaces = []
            self.buttons.clear()

        elif self.status == "main":
            self.surfaces = []
            self.buttons.clear()
            self.surfaces.append(self.title)
            self.buttons.append(Button((WIDTH - 300)//2, 150, 300, 75, button_font, "Nouvelle partie", self.create_game))
            self.buttons.append(Button((WIDTH - 300)//2, 250, 300, 75, button_font, "Sauvegardes", self.change_status, False, "saves"))
            self.buttons.append(Button((WIDTH - 300)//2, 350, 300, 75, button_font, "Paramètres", self.change_status, False,"settings"))
            for element in self.buttons:
                self.surfaces.append(element)
                
        elif self.status == "settings":
            self.surfaces = []
            self.buttons.clear()
            settings = get_actual_settings()
            index_left, index_right = 0,0
            for (key, value) in settings.items():
                #Première colonne (gauche) : choix des touches
                if key[0] == "k":
                    surf = self.keys_names_rendered[settings_name[key]]
                    surf.rect = surf.image.get_rect(topleft=(20,(index_left+1)*50))
                    self.surfaces.append(surf)
                    self.buttons.append(Button(200, (index_left+1)*50 - 15, 350,40, button_font, str(value), self.change_key, False,key))
                    index_left += 1
                else:
                    surf = self.keys_names_rendered[settings_name[key]]
                    surf.rect = surf.image.get_rect(topleft=(WIDTH//2 + 20,(index_right+1)*50))
                    self.surfaces.append(surf)
                    index_right += 1
                
            for button in self.buttons:
                self.surfaces.append(button)
            
        elif self.status == "saves":
            pass

    def change_status(self,status):
        """Change le status du menu

        Args:
            status (str): Nouveau status
        """
        self.status = status
        self.handle()
        return status

    def change_key(self,key):
        return True
        

    def create_game(self,*args):
        """Fonction appelée lors du click du bouton "nouvelle partie"

        Returns:
            string: Renvoie l'action à effectuer dans la classe Main
        """
        self.change_status("hidden")

        return "first load"
    

class Button:
    def __init__(self, x, y, width, height, font, buttonText='Button', onclickFunction=None, onePress=False, *args):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = font
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.args = args

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }

        self.image = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = self.font.render(buttonText, True, (20, 20, 20))

        self.alreadyPressed = False

    def process(self):
        result = None
        mousePos = pygame.mouse.get_pos()
        
        self.image.fill(self.fillColors['normal'])
        if self.rect.collidepoint(mousePos):
            self.image.fill(self.fillColors['hover'])

            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.image.fill(self.fillColors['pressed'])

                if self.onePress:
                    print(self.args)
                    result = self.onclickFunction(*self.args)

                elif not self.alreadyPressed:
                    result = self.onclickFunction(*self.args)
                    self.alreadyPressed = True

            else:
                self.alreadyPressed = False

        self.image.blit(self.buttonSurf, [
            self.rect.width/2 - self.buttonSurf.get_rect().width/2,
            self.rect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        return result