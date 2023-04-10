import pygame
from settings import *

class Case(pygame.sprite.Sprite):
    def __init__(self, x, y, groupes, texture, surface=pygame.Surface((CASE_SIZE, CASE_SIZE)), basey=None):
        """Objet de base Case : sert à contenir une case de la map. Hérite de pygame.sprite.Sprite

        Args:
            x (int): position x
            y (int): position y 
            groupes (list): liste de pygame.sprites.Group auxquels ajouter la case
            texture (pygame.image): texture de la case (utilisée pour l'affichage dans le cas où l'image n'est pas override)
            surface (pygame.Surface, optional): Surface personnalisée pour la case. Par défaut une surface de la taille standard d'une case.
            basey (int, optional): Position y de la base de la case pour l'affichage (si =None, utilisation de la base de la surface) . Defaults to None.
        """
        super().__init__(groupes) #ajoute le sprite au groupe passé en paramètre
        self.image = texture
        self.x = x
        self.y = y
        self.surface = surface.get_rect(topleft=(x,y))

        if not basey:
            self.basey = self.surface.bottom
        else:
            self.basey = basey
        
class Trigger(Case):
    def __init__(self, x, y, groupes, texture,trigger_func, surface=pygame.Surface((CASE_SIZE, CASE_SIZE)), basey=None, *args):
        """Case spéciale contenant une fonction activée lorsque le joueur est dans la surface de la case

        Args:
            x (int): position x
            y (int): position y 
            groupes (list): liste de pygame.sprites.Group auxquels ajouter la case
            texture (pygame.image): texture de la case (utilisée pour l'affichage dans le cas où l'image n'est pas override)
            trigger_func (func): fonction appelée lorsque le joueur est dans la zone de la case.
            surface (pygame.Surface, optional): Surface personnalisée pour la case. Par défaut une surface de la taille standard d'une case.
            basey (int, optional): Position y de la base de la case pour l'affichage (si =None, utilisation de la base de la surface) . Defaults to None.
        """
        super().__init__(x, y, groupes, texture, surface, basey)
        self.func = trigger_func
        self.args = args
        self.activated = False
        
        
    def handle(self, player):
        """Appelle la fonction assignée au bloc trigger si le player est sur la case

        Args:
            player (Player): Objet du joueur 

        Returns:
            any: renvoie le return de la fonction
        """
        if player.rect.colliderect(self.surface):
            if self.activated==False:
                self.activated = True
                return self.func(*self.args)
        elif self.activated:
            self.activated = False