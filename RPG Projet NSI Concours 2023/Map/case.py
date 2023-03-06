import pygame
from settings import *

class Case(pygame.sprite.Sprite):
    def __init__(self, x, y, groupes, texture, surface=pygame.Surface((CASE_SIZE, CASE_SIZE)), basey=None):
        super().__init__(groupes) #ajoute le sprite au groupe passé en paramètre
        self.image = texture
        self.x = x
        self.y = y
        if self.image:
            self.surface = self.image.get_rect(topleft=(x,y))
            self.surface.height = 40
        else:
            self.surface.topleft=(x,y)
        if not basey:
            self.basey = self.surface.centery
        else:
            self.basey = basey
        