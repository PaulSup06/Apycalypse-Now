from entity import Entity
import pygame
from settings import *
from inventaire import Item
import random

class Enemy(Entity):
    def __init__(self, x, y, image, groupes, collision_blocks, textures, movement_type, name, item_group, speed=None, damages=None, health=None, movement_condition=True):
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
        self.item_images = load_item_imgs()
        self.item_group = item_group

        self.textures = textures[name]
        if speed:
            self.speed = speed
        else:
            self.speed = enemy_caracteristics[self.name]["speed"]
        if damages:    
            self.damages = damages
        else:
            self.damages = enemy_caracteristics[self.name]["damages"]
        if health:    
            self.health = health
            self.max_health = health
        else:
            self.health = enemy_caracteristics[self.name]["health"]
            self.max_health = enemy_caracteristics[self.name]["health"]

        self.attack_cooldown = 60
        self.movement_condition = movement_condition
        self.direction=1
        self.action = "idle"
        self.animation_counter = 0
        #gestion fin de la vie de l'ennemi
        self.death_cooldown = 40
        self.stunt_cooldown = 20 
        
    def move(self, player):
        """Gestion du mouvement de l'ennemi ainsi que de ses collisions et états

        Args:
            player (player object): objet du joueur pour les colisions et la gestion des dégats

        Returns:
            int: dégats infligés
        """
        if self.rect.colliderect(player.rect) and player.invincibility == False and self.action !="attack" and self.action!="death" and self.action !='stunt':            
            self.action = "attack"
            self.animate()
            return self.damages
        
        if self.action == "attack":            
            self.attack_cooldown -= 1
            if self.attack_cooldown<=0:
                self.attack_cooldown = 60
                self.action = "idle"
        
        elif self.action == "death":
            self.death_cooldown -= 1
            if self.death_cooldown <= 0:
                self.drop_item()
                self.kill()

        elif self.action == "stunt":
            self.stunt_cooldown -= 1
            if self.stunt_cooldown <= 0:
                self.action = "idle"

        elif self.movement_condition:
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

            if not self.check_collision(self.collision_blocks, "vertical", self.movement.x * self.speed):
                self.y += self.movement.y * self.speed
            else:
                self.change_direction()
                
            self.rect.topleft = (self.x,self.y)
            self.action = "move"

        else:
            self.action = "idle" 

        self.animate()

    def animate(self):
        """Sous fonction de move(), s'occupe plus précisément des animations de l'ennemi
        """
        if self.action == "attack" or self.action == "death":
            self.image = self.textures[self.action][0]
        elif self.action == "stunt":
            self.image = self.textures["idle"][0]
        else:
            self.image = self.textures[self.action][self.animation_counter//enemy_anim_duration]
            self.animation_counter +=1  
            if self.animation_counter//enemy_anim_duration > len(self.textures[self.action])-1:
                self.animation_counter = 0


    def change_direction(self):
        """Change la direction de déplacement de l'ennemi (utilisé seulement pour déplacements en ligne droite)
        """
        self.direction *= -1

    def hit(self,damages,stunt=20):
        """Méthode appelée pour infliger des dégats à l'ennemi (généralement par le joueur)

        Args:
            damages (int): nombre de dégats à infliger
            stunt (int, optional): nombre de frames pendant lesquels l'ennemi ne pourra pas bouger (étourdi). Defaults to 20.
        """
        self.health -= damages
        self.action = "stunt"
        self.stunt_cooldown = stunt
        if self.health <= 0:
            self.action = "death"
            
    def drop_item(self):
        drop_items = enemy_caracteristics[self.name]["drops"]
        for item in drop_items:
            tirage = random.randint(1,100)
            if item["drop_rate"]<=tirage:
                offset = random.randint(-10,10)
                positive = random.choice((-0.2,0.2))
                Item(self.x+(offset*positive),self.rect.bottom + offset, self.item_images[item["name"]], self.item_group, item["name"], item["drop_count"])