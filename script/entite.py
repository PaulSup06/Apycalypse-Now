import pygame
from settings import *

class Entite(pygame.sprite.Sprite):
    def __init__(self, x,y, image, groupes):
        super().__init__(groupes)
        self.x = x
        self.y = y
        self.image = image
        self.surface = self.image.get_rect()

    def check_collision(self, collidegroup, direction, value):
        """Verifie les collisions avant de bouger l'entité

        Args:
            collidegroup (pygame.sprite.Group): Groupe d'entités avec lesquelles vérifier la collision
            direction (str): vertical ou horizontal
            value (int): valeur du déplacement prévu

        Returns:
            Bool: True si l'entité à collide avec une autre entité (utile pour les mobs)
        """
        collided = False
        for case in collidegroup:    
            if direction=="vertical" and self.surface.right > case.surface.x and self.x < case.surface.right:
                if value<0 :
                    if self.y + value <= case.surface.bottom and self.y + value >= case.surface.y:
                        self.y = case.surface.bottom + hitbox_margin
                        collided = True
                elif value>0:
                    if self.surface.bottom+value >= case.surface.y and self.surface.bottom+value <= case.surface.bottom:
                        self.bottom = case.surface.top - hitbox_margin
                        collided = True

            if direction=="horizontal" and self.surface.bottom > case.surface.top and self.y < case.surface.bottom:
                if value<0:
                    if self.surface.left + value <= case.surface.right and self.surface.right + value >= case.surface.left:
                        self.surface.left = case.surface.right + hitbox_margin
                        collided = True
                elif value>0:
                    if self.surface.right+value >= case.surface.x and self.x+value <= case.surface.right:
                        self.surface.right = case.surface.left - hitbox_margin
                        collided = True

        return collided
        