import pygame
from settings import *

class Case(pygame.sprite.Sprite):
    def __init__(self, x, y, groupes, texture,  surface=pygame.Surface((CASE_SIZE, CASE_SIZE))):
        super().__init__(groupes) #ajoute le sprite au groupe passé en paramètre
        