from entity import Entity
import pygame
from settings import *

class Lever(Entity):
    def __init__(self, x, y, image, groupes, textures, function_to_call, main_elmt, name,id=-1,basey=None, *args):
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
        self.image = self.textures[0]
        self.activated = False
        self.function_to_call = getattr(main_elmt,function_to_call)
        self.args = args
        self.animation_counter_fps = 0
        self.player_near = False
        self.name = name
        self.id = id
        self.is_animited = False
        if basey:
            self.basey = basey


    def handle(self,player,surface, offset, settings, has_manivelle):
        if player.check_distance_to(self.surface.center, interact_distance):
            self.player_near = True
            self.show_indicator(surface, offset, settings)
        else:
            self.player_near = False
          
    def show_indicator(self,surface, offset, settings):
        surface.blit(font2.render(f"[{pygame.key.name(int(settings['k_interact'])).upper()}] pour actionner",1,"white"), (self.x - offset.x, self.y +50 - self.image.get_height() - offset.y))

    def interact(self):
        if not self.is_animited:
            global actual_sound_channel 
            self.is_animited = True

            # animation levier activé
            #inversion valeur d'activation du levier
            self.activated = self.activated == False
            
            # joue son trigger
            pygame.mixer.Channel(actual_sound_channel).play(pygame.mixer.Sound(os.path.join(music_folder, "switch\\lever.mp3")))
            actual_sound_channel = 1 if actual_sound_channel >= 999 else actual_sound_channel + 1

            self.function_to_call(*self.args)
            self.animate()
        
    def animate(self):
        """ Anim levier
        """
        if self.is_animited:

            # anime vers la droite
            if self.activated:
                self.animation_counter_fps += 1
                self.image = self.textures[self.animation_counter_fps // (FPS//5)]

                if self.animation_counter_fps // (FPS//5) == 2:
                    self.is_animited = False

            # anime vers la gauche
            if not self.activated:
                self.animation_counter_fps -= 1
                self.image = self.textures[self.animation_counter_fps // (FPS//5)]

                if self.animation_counter_fps // (FPS//5) == 0:
                    self.is_animited = False


class PressurePlate(Entity):
    def __init__(self, x, y, image, groupes, textures, function_to_call, main_elmt, name,id=-1,*args):
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
        self.image = self.textures[0]
        self.activated = False
        self.name = name
        self.id = id
        self.is_animating = False

        self.basey = self.surface.top # pressure plate apparait derrière le joueur
        self.function_to_call = getattr(main_elmt,function_to_call)
        self.args = args
        self.animation_counter_fps = 0
        self.player_on_it = False

    def handle(self, player, surface, offset, settings, has_manivelle):
        global actual_sound_channel
        if self.rect.colliderect(player.rect):
            if not self.player_on_it:
                self.player_on_it = True
                self.activated = True
                self.is_animating = True
                # joue son trigger
                pygame.mixer.Channel(actual_sound_channel).play(pygame.mixer.Sound(os.path.join(music_folder, "switch\\pressureplate.mp3")))
                actual_sound_channel = 1 if actual_sound_channel >= 999 else actual_sound_channel + 1
                
                self.function_to_call(*self.args)
                self.animate()
        else:
            if self.player_on_it:
                self.player_on_it = False
                self.activated = False
                self.is_animating = True
                # joue son trigger
                pygame.mixer.Channel(actual_sound_channel).play(pygame.mixer.Sound(os.path.join(music_folder, "switch\\pressure_plate_up.mp3")))
                actual_sound_channel = 1 if actual_sound_channel >= 999 else actual_sound_channel + 1
                self.animate()
                


    def animate(self):
        """ Anim pressure plate
        """
        if self.is_animating :
            if self.activated:
                self.animation_counter_fps += 1
                self.image = self.textures[self.animation_counter_fps // (FPS//14)]

                if self.animation_counter_fps // (FPS//14) >= 3:
                    #self.action = "unpressed"
                    self.animation_counter_fps = 0
                    self.is_animating = False

            if not self.activated:
                self.animation_counter_fps += 1
                self.image = self.textures[3 - self.animation_counter_fps // (FPS//14)]

                if self.animation_counter_fps // (FPS//14) >= 3:
                    self.action = "pressed"
                    self.animation_counter_fps = 0
                    self.is_animating = False



class Manivelle(Entity):
    def __init__(self, x, y, image, groupes, textures, function_to_call, main_elmt, name, id,manivelle=True,height=0, *args):
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
        self.activated = False
        if manivelle:
            self.action = "manivelle"
            self.image = self.textures[1]
        self.name = name
        self.id = id
        
        self.function_to_call = getattr(main_elmt,function_to_call)
        self.args = args
        self.animation_counter_fps = 0
        self.player_near = False
        self.is_off = True
        
        self.basey = self.y + (height+ 1)*CASE_SIZE
        self.have_manivelle = False

    def handle(self,player,surface, offset, settings, have_manivelle):
        if player.check_distance_to(self.surface.center, interact_distance) and self.is_off:
            self.player_near = True
            self.show_indicator(surface, offset, settings, have_manivelle)
        else:
            self.player_near = False
        self.animate()

          
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
            pygame.mixer.Channel(actual_sound_channel).play(pygame.mixer.Sound(os.path.join(music_folder, "switch\\manivelle_place.mp3")))
            actual_sound_channel = 1 if actual_sound_channel >= 999 else actual_sound_channel + 1

            return "remove_manivelle_from_player_inventory"
        
        if self.action ==  "manivelle" :
            # tourne la manivelle

            # animation manivelle tournée
            self.is_off = False
            
            self.action = "turning"
            self.activated = True
            self.animation_counter_fps =  1
            
            # joue son trigger
            pygame.mixer.Channel(actual_sound_channel).play(pygame.mixer.Sound(os.path.join(music_folder, "switch\\manivelle.mp3")))
            actual_sound_channel = 1 if actual_sound_channel >= 999 else actual_sound_channel + 1

            self.function_to_call(*self.args)
            
        
    def animate(self):
        """Anime manivelle
        """
        if self.action == "turning":
            self.animation_counter_fps += 1
            self.image = self.textures[self.animation_counter_fps // (FPS//5)]

            if self.animation_counter_fps // (FPS//5) == 2:
                self.action = "idle"
                self.animation_counter_fps = 0

