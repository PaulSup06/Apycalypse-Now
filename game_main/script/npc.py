import pygame
import os
from settings import *
from inventaire import Item

from entity import Entity

class Npc(Entity):
    def __init__(self, x, y, image, groupes, name, talkable=False, indicator="...", first_dialog="1"):
        """Entité spécifiée comme étant un NPC (ou PNJ), capable d'intéragir avec le joueur. Hérite de la class Entity.

        Args:
            x (int): position x
            y (int): position y
            image (pygame.image): image par défaut du npc
            groupes (list): list de pygame.sprite.Group auxquels ajouter le Npc
            name (str): nom du npc (pour les dialogues)
            talkable (bool, optional): Disponibilité du npc par défaut. Defaults to False.
            indicator (str, optional): En tête par défaut lorsque le joueur s'approche. Defaults to "...".
            first_dialog (str, optional): Index du premier dialogue à prononcer. Defaults to "1".
        """
        super().__init__(x, y, image, groupes)
        self.name = name
        self.item_imgs = load_item_imgs()
        self.basey = self.y + self.image.get_height()
        self.change_state(talkable, indicator, first_dialog)
        

    def change_state(self,state, indicator, next_dialog_id):
        """Change l'état du NPC et son en-tête

        Args:
            state (Bool): Etat du NPC si disponible pour dialogue ou non
            indicator (str): Change l'affichage de l'en-tête du NPC
            next_dialog (int/str): Charge le prochain dialogue du NPC
        """
        self.is_talkable = state
        self.indicator = indicator
        self.next_dialog = next_dialog_id
        self.indicator_rendered = font1.render(self.indicator,1,"black").convert_alpha()

    def get_state(self):
        """Retourne l'état du NPC avec son indicateur et l'id de son prochain dialogue

        Returns:
            _type_: _description_
        """
        return self.is_talkable, self.indicator, self.next_dialog
    
    def show_indicator(self, surface, offset, settings,player):
        """Affiche l'en-tête du npc

        Args:
            surface (pygame.Surface): Destination d'affichage (screen)
            offset (Vector2): Camera offset pour l'affichage
        """
        indicator_rect = pygame.Rect(self.x + self.surface.width + 5 - offset.x, self.y - 15 - offset.y, self.indicator_rendered.get_width()+10, self.indicator_rendered.get_height()+10)
        indicator_rect_surf = pygame.Surface(indicator_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(indicator_rect_surf,(240,240,240,180),indicator_rect_surf.get_rect(),0,5)
        surface.blit(indicator_rect_surf, indicator_rect)
        pygame.draw.rect(surface,"black",indicator_rect,1,5)
        surface.blit(self.indicator_rendered, (self.x + self.surface.width + 10 - offset.x, self.y - 10 - offset.y))
        if self.is_talkable and self.check_distance_to(player.rect.center,interact_distance):
            surface.blit(font2.render(f"[{pygame.key.name(int(settings['k_interact'])).upper()}] pour parler" ,1,"black"), (self.x + self.surface.width + 5 - offset.x, self.y - 5 + indicator_rect.height - offset.y))

    def interact(self):

        return self.next_dialog, self.name
    
    def drop_item(self, item_name, count,item_group):
        Item(self.rect.centerx,self.rect.bottom + 20, self.item_imgs[item_name], item_group,item_name, count)

class Door(Entity):
    def __init__(self, x, y, groupes, imgs, id=-1, locked=False):
        """Objet Door : porte coulissante du labo, s'ouvre lors de l'arrivée du joueur, déverouillable. Hérite de la class Entity.

        Args:
            x (int): position x
            y (int): position y
            groupes (list): list de pygame.sprite.Group auxquels ajouter le Npc
            id (int): id de la porte (correspond à un terminal pour la déverrouiller). Par défaut -1 si non assignée (pas verouillable)
            imgs (list): liste des images de la porte (5 frames de fermé à ouvert)
            locked (bool, optional): Verrouillage de la porte. Defaults to False.
        """
        self.images = imgs
        self.image = self.images[0]
        super().__init__(x, y, self.image, groupes)
        self.surface = pygame.Rect(self.x, self.y+CASE_SIZE,CASE_SIZE*2,32)
        self.basey = self.surface.bottom
        self.id = int(id)
        self.locked = locked
        self.counter = 0
        
    
    def update(self, player):
        """Ouvre ou ferme la porte en fonction de la position du joueur

        Args:
            player (Player object): Joueur 
        """
        if not self.locked:
            if player.check_distance_to((self.x + CASE_SIZE, self.y + CASE_SIZE), door_unlock_range):
                if self.counter//5 < 4:
                    self.counter +=1
                if self.counter//5==4:
                    self.surface = pygame.Rect(self.x,self.y,0,0)
            else:
                if self.counter > 0:
                    self.counter -= 1
                    self.surface = pygame.Rect(self.x, self.y+CASE_SIZE,CASE_SIZE*2,32)
        else:
            if self.counter > 0:
                    self.counter -= 1
                    self.surface = pygame.Rect(self.x, self.y+CASE_SIZE,CASE_SIZE*2,32)   
        self.image = self.images[self.counter//5]
            
    def unlock(self):
        self.locked = False
        
    def lock(self):
        self.locked = True