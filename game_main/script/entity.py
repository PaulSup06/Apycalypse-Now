import pygame
from settings import *

class Entity(pygame.sprite.Sprite):
    def __init__(self, x,y, image, groupes, hitbox=None):
        """Objet de base pour tout objet mobile ou intéractif du jeu.
        Hérite de la class pygame.sprite.Sprite 

        Args:
            x (int): position x
            y (int): position y
            image (pygame.image): image par défaut de l'entité (habituellement override mais si image unique peut être utile)
            groupes (list): list des pygame.sprite.Group() auxquels ajouter l'Entity
            hitbox (pygame.Rect, optional): Rectangle utilisé pour les collisions. Si non spécifié, utilisation de la surface de l'image.
            smaller_collision (bool, optional): Pour le trigger, si la collision est plus petite pour cette entité
        """
        super().__init__(groupes)
        self.x = x
        self.y = y
        self.image = image
        self.surface = self.image.get_rect(topleft=(x,y))
    
        self.basey = self.surface.centery
        if hitbox:
            self.rect = hitbox
        else:
            self.rect = self.surface

    def check_collision(self, collidegroup, direction, value):
        """Verifie les collisions avant de bouger l'entité + EMPECHE CELUI-CI DE BOUGER LE CAS ECHEANT
        (place l'entité à sa position autorisée maximale si collision)

        Args:
            collidegroup (pygame.sprite.Group): Groupe d'entités avec lesquelles vérifier la collision
            direction (str): vertical ou horizontal
            value (int): valeur du déplacement prévu

        Returns:
            Bool: True si l'entité à collide avec une autre entité (utile pour les mobs)
        """
        collided = False
        for case in collidegroup:    
            if direction=="vertical" and self.rect.right > case.surface.x and self.rect.left < case.surface.right:
                if value<0 :
                    if self.rect.top + value <= case.surface.bottom and self.rect.top + value >= case.surface.y:
                        self.rect.top = case.surface.bottom
                        collided = True
                elif value>0:
                    if self.rect.bottom+value >= case.surface.y and self.rect.bottom+value <= case.surface.bottom:
                        self.bottom = case.surface.top
                        collided = True

            if direction=="horizontal" and self.rect.bottom > case.surface.top and self.rect.top < case.surface.bottom:
                if value<0:
                    if self.rect.left + value <= case.surface.right and self.rect.right + value >= case.surface.left:
                        self.rect.left = case.surface.right
                        collided = True
                elif value>0:
                    if self.rect.right+value >= case.surface.x and self.rect.left+value <= case.surface.right:
                        self.rect.right = case.surface.left
                        collided = True

        return collided
    
    def check_distance_to(self, target_pos, distance_max):
        """Vérifie si la distance entre l'entité et une certaine position est inférieure à une valeur donnée

        Args:
            target_pos (tuple): (pos x, pos y)
            distance_max (int): distance en pixels maximum pour laquelle la fonction renvoie True

        Returns:
            Bool: True si la distance est inférieure à distance_max, sinon False
        """
        distance = pygame.math.Vector2()
        distance.x = self.rect.left - target_pos[0]
        distance.y = self.rect.top - target_pos[1]

        if distance.length()<=distance_max:
            return True
        else:
            return False
        
        