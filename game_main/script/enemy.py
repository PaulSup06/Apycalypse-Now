from entity import Entity
import pygame

class Enemy(Entity):
    def __init__(self, x, y, image, groupes, collision_blocks, textures, movement_type, name, speed, movement_condition=True):
        """Enemy héritant de la classe Entité, est hostile au joueur

        Args:
            x (int): pos x
            y (int): pos y
            image (pygame.image): image par défaut (utile uniquement pour la classe Entity)
            groupes (list): liste de groupes auquels appartient l'Enemy
            collision_blocks (pygame.group.Group): Blocks de collisions pour les déplacements
            textures (dict): dictionnaire contenant les textures rendues pygame
            movement_type (string): Types de mouvements possibles : -ligne_h -ligne_v -to_player 
            TODO: implémenter -pathfind_to_player -teleport ???
                        
            name (str): Nom de la classe de l'ennemi
            speed (int): Vitesse de déplacement de l'ennemi
            movement_condition (bool, optional): Condition pour laquelle l'ennemi se déplace. Defaults to True.
        """ 
        super().__init__(x, y, image, groupes)
        self.collision_blocks = collision_blocks
        self.movement_type = movement_type
        self.name = name
        self.textures = textures[name]
        self.speed = speed
        self.movement_condition = movement_condition
        self.direction=1
        self.action = "idle"
        
    def move(self, player):
        
        
        if self.movement_condition:
            self.movement = pygame.Vector2()
            
            if self.movement_type == "ligne_h":
                self.movement.x += self.direction
            elif self.movement_type == "ligne_v":
                self.movement.y += self.direction
            elif self.movement_type == "to_player":
                player_pos = player.x, player.y
                self.movement.x = player_pos[0] - self.x
                self.movement.y = player_pos[1] - self.y
                self.movement.normalize()
            
            if not self.check_collision(self.collision_blocks, "horizontal", self.movement.x * self.speed):
                self.x += self.movement.x * self.speed
            else:
                self.change_direction()
            if not self.check_collision(self.collision_blocks, "horizontal", self.movement.x * self.speed):
                self.y += self.movement.y * self.speed
            else:
                self.change_direction()
                
            self.rect.topleft = (self.x,self.y)
        
    def change_direction(self):
        self.direction *= -1