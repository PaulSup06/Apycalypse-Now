from entity import Entity
import pygame
from settings import *
from inventaire import Item
import random

"""

        UTILISATION SUR TILED:
        1 - CREE UN LAYER DU NOM DE "switches"
        2 - LE NOM DE LA FONCTION SE TROUVANT DANS MAIN DOIT ETRE INSCRIT DANS LA PROPRIETEE "classe" DU LAYER
        TOUT LES SWITCHES DANS CE LAYER EXECUTERONS LA MEME FONCTION
        Je ne pouvais pas faire autrement, ou alors on check le x et y du levier pour l'attribuer à sa fonction respectif
        

"""

class Lever(Entity):
    def __init__(self, x, y, image, groupes, textures, function_to_call, name):
        """Levier héritant de la classe Entité, est utile au joueur
        Args:
            x (int): pos x
            y (int): pos y
            image (pygame.image): image par défaut (utile uniquement pour la classe Entity)
            groupes (list): liste de groupes auquels appartient l'Enemy
            textures (dict): dictionnaire contenant les textures rendues pygame         
            function_to_call (str): Nom de la fonction à appeler lorsque l'interrupteur est enclanché
        """ 
        super().__init__(x, y, image, groupes)
        self.textures = textures
        self.action = "idle"
        self.function_to_call = function_to_call
        self.animation_counter_fps = 0
        self.player_near = False
        self.name = name
        self.is_off = True

    def handle(self,player,surface, offset, settings, has_manivelle):
        if player.check_distance_to(self.surface.center, interact_distance) and self.is_off:
            self.player_near = True
            self.show_indicator(surface, offset, settings)
        else:
            self.player_near = False
          
    def show_indicator(self,surface, offset, settings):
        surface.blit(font2.render(f"[{pygame.key.name(int(settings['k_interact'])).upper()}] pour actionner",1,"white"), (self.x - offset.x, self.y +50 - self.image.get_height() - offset.y))

    def interact(self):
        if self.is_off:
            global actual_sound_channel 

            # animation levier activé
            self.is_off = False
            
            self.action = "triggered"
            # joue son trigger
            pygame.mixer.Channel(actual_sound_channel).play(pygame.mixer.Sound(os.path.join(sound_folder, "switch\\lever.mp3")))
            actual_sound_channel = 1 if actual_sound_channel >= 999 else actual_sound_channel + 1

            return self.function_to_call
        
    def animate(self):
        """ Anim levier
        """
        if self.action == "triggered":
            self.animation_counter_fps += 1
            self.image = self.textures[self.animation_counter_fps // (FPS//5)]

            if self.animation_counter_fps // (FPS//5) == 2:
                self.action = "idle"
                self.animation_counter_fps = 0


class PressurePlate(Entity):
    def __init__(self, x, y, image, groupes, textures, function_to_call, name):
        """PressurePlate héritant de la classe Entité, est utile au joueur

        Args:
            x (int): pos x
            y (int): pos y
            image (pygame.image): image par défaut (utile uniquement pour la classe Entity)
            groupes (list): liste de groupes auquels appartient l'Enemy
            textures (dict): dictionnaire contenant les textures rendues pygame         
            function_to_call (str): Nom de la fonction à appeler lorsque l'interrupteur est enclanché
        """ 
        super().__init__(x, y, image, groupes,hitbox=pygame.Rect(x+15,y+8, 40, 40))
        self.textures = textures
        self.action = "idle"
        self.name = name

        self.basey = self.surface.top # pressure plate apparait derrière le joueur
        self.function_to_call = function_to_call
        self.animation_counter_fps = 0
        self.is_off = True

    def handle(self,player, surface, offset, settings, has_manivelle): # /!\ même si inutilisé on doit garder les paramètres là pour le trigger depuis main /!\
        global actual_sound_channel 

        if self.rect.colliderect(player.rect) and self.action == "idle" :            
            if self.is_off:
                global actual_sound_channel 

                # animation pressurplate activé
                self.is_off = False
                
                self.action = "triggered"
                # joue son trigger
                pygame.mixer.Channel(actual_sound_channel).play(pygame.mixer.Sound(os.path.join(sound_folder, "switch\\pressureplate.mp3")))
                actual_sound_channel = 1 if actual_sound_channel >= 999 else actual_sound_channel + 1

                return self.function_to_call
          
    def animate(self):
        """ Anim pressure plate
        """
        if self.action == "triggered":
            self.animation_counter_fps += 1
            self.image = self.textures[self.animation_counter_fps // (FPS//14)]

            if self.animation_counter_fps // (FPS//14) >= 3:
                self.action = "idle"
                self.animation_counter_fps = 0


class Manivelle(Entity):
    def __init__(self, x, y, image, groupes, textures, function_to_call, name, manivelle):
        """Enemy héritant de la classe Entité, est hostile au joueur

        Args:
            x (int): pos x
            y (int): pos y
            image (pygame.image): image par défaut (utile uniquement pour la classe Entity)
            groupes (list): liste de groupes auquels appartient l'Enemy
            textures (dict): dictionnaire contenant les textures rendues pygame         
            function_to_call (str): Nom de la fonction à appeler lorsque l'interrupteur est enclanché
            name (str) : nom du type de switch (manivelle)
            anivelle (bool) : manivelle équipée par défaut
        """ 
        super().__init__(x, y, image, groupes)
        self.textures = textures
        self.action = "idle"
        if manivelle:
            self.action = "manivelle"
            self.image = self.textures[1]
        self.name = name

        self.function_to_call = function_to_call
        self.animation_counter_fps = 0
        self.player_near = False
        self.is_off = True
        
        self.have_manivelle = False

    def handle(self,player,surface, offset, settings, have_manivelle):
        if player.check_distance_to(self.surface.center, interact_distance) and self.is_off:
            self.player_near = True
            self.show_indicator(surface, offset, settings, have_manivelle)
        else:
            self.player_near = False
        

          
    def show_indicator(self,surface, offset, settings, have_manivelle):
        message = ("Il vous faut une manivelle" if have_manivelle == False and self.action == "idle" else  f"[{pygame.key.name(int(settings['k_interact'])).upper()}] pour placer la manivelle") if self.action != "manivelle" else f"[{pygame.key.name(int(settings['k_interact'])).upper()}] pour actionner"
        self.have_manivelle = have_manivelle
        surface.blit(font2.render(message,1,"white"), (self.x - offset.x, self.y +50 - self.image.get_height() - offset.y))

    def interact(self):
        global actual_sound_channel 

        if self.have_manivelle and self.action == "idle":
            # place la manivelle
            
            self.action = "manivelle"
            self.image = self.textures[1]
            # joue son trigger
            pygame.mixer.Channel(actual_sound_channel).play(pygame.mixer.Sound(os.path.join(sound_folder, "switch\\manivelle_place.mp3")))
            actual_sound_channel = 1 if actual_sound_channel >= 999 else actual_sound_channel + 1

            return "remove_manivelle_from_player_inventory"
        
        if self.action ==  "manivelle" :
            # tourne la manivelle

            # animation manivelle tournée
            self.is_off = False
            
            self.action = "turning"
            self.animation_counter_fps =  1
            # joue son trigger
            pygame.mixer.Channel(actual_sound_channel).play(pygame.mixer.Sound(os.path.join(sound_folder, "switch\\manivelle.mp3")))
            actual_sound_channel = 1 if actual_sound_channel >= 999 else actual_sound_channel + 1

            return self.function_to_call
        
    def animate(self):
        """Sous fonction de move(), s'occupe plus précisément des animations de l'ennemi
        """
        if self.action == "turning":
            self.animation_counter_fps += 1
            self.image = self.textures[self.animation_counter_fps // (FPS//5)]

            if self.animation_counter_fps // (FPS//5) == 2:
                self.action = "idle"
                self.animation_counter_fps = 0

