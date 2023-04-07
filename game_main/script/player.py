from settings import *
from entity import *
from debug import *

class Player(Entity):
    def __init__(self, x, y, groupes, collision_blocks, player_life, max_life, weapon=None):
        """Objet Player : objet principal controlable par le joueur

        Args:
            x (int): position x
            y (int): position y
            groupes (list de pygame.sprite.Group): groups auxquels ajouter le joueur
            collision_blocks (pygame.sprite.Group): blocs de collision pour les déplacements 
            player_life (int): vie restante au joueur
            weapon (à déterminer, optional): Arme du joueur lors de sa génération. Defaults to None.
        """
        self.player_imgs = load_player_imgs()
        self.image = self.player_imgs["up"]["up_0.png"]
        super().__init__(x, y, self.image, groupes)
        self.surface = self.image.get_rect(topleft=(x,y))
        self.rect = pygame.Rect(self.x, self.y + 10, 64, self.surface.height - hitbox_offset * 2) #à modif
        self.collision_blocks = collision_blocks
        self.basey = self.rect.bottom
        self.direction = "down"
        self.movement = pygame.Vector2()
        self.animation_counter = 0

        #variables de gameplay
        self.life = player_life
        self.speed_multiplier = 1 
        self.strength_multiplier = 1 
        self.invincibility = False
        self.max_life = max_life
        self.attacking = False
        self.weapon = weapon
        self.attack_counter = 0
        if self.weapon:
            self.attack_cooldown = self.weapon.attack_cooldown
        else:
            self.attack_cooldown = default_player_attack_cooldown
        

    def move(self, keys, settings):
        """Déplacement et collisions du personnage principal

        Args:
            keys (list): Liste des touches pressées par le joueur
            settings (dict): dictionnaire des touches paramétrées
        """
        if not self.attacking:
            self.movement = pygame.math.Vector2()
            self.movement.x, self.movement.y = 0,0
            if keys[int(settings["k_left"])]:
                self.movement.x += -1
                self.direction = "left"
            if keys[int(settings["k_right"])]:
                self.movement.x += 1
                self.direction = "right"
            if keys[int(settings["k_up"])]:
                self.movement.y += -1
                self.direction = "up"
            if keys[int(settings["k_down"])]:
                self.movement.y += 1
                self.direction = "down"

            if self.movement.length() != 0:
                self.movement = self.movement.normalize()
            
            if self.check_collision(self.collision_blocks, "horizontal", self.movement.x * (playerspeed * self.speed_multiplier)) == False:
                self.x += self.movement.x * (playerspeed * self.speed_multiplier)
                
            if self.check_collision(self.collision_blocks, "vertical", self.movement.y * (playerspeed * self.speed_multiplier)) == False:
                self.y += self.movement.y * (playerspeed * self.speed_multiplier)
                            
            self.x = round(self.x)
            self.y = round(self.y)
            
            self.surface.topleft = (self.x,self.y)
            self.rect.topleft = (self.x, self.y + hitbox_offset)
            self.basey = self.surface.centery

    def update(self):
        """Gère les animations du joueur en fonction de ses déplacemens
        """
        if not self.attacking:
            if self.movement.length() == 0:
                self.image = self.player_imgs[self.direction+"_idle"]["idle_"+self.direction+".png"]
                self.animation_counter = 0
            else:
                self.image = self.player_imgs[self.direction][self.direction+"_"+str(self.animation_counter//walk_anim_duration)+".png"]
                self.animation_counter +=1
                if self.animation_counter >= walk_anim_duration * 4:
                    self.animation_counter = 0
        else:
            if self.attack_counter < (1/3)*self.attack_cooldown:
                self.image = self.image = self.player_imgs[self.direction+"_idle"]["idle_"+self.direction+".png"]
            elif self.attack_counter < (2/3)*self.attack_cooldown:
                self.image = self.image = self.player_imgs[self.direction+"_attack"]["attack_"+self.direction+".png"]
            else:
                self.image = self.image = self.player_imgs[self.direction+"_idle"]["idle_"+self.direction+".png"]
            self.attack_counter +=1
            if self.attack_counter >= self.attack_cooldown:
                self.attacking = False
        
        # TODO : dessine la bubble (si le joueur est invincible)
        # "..\\textures\\player\\misc\\invincibility_bubble.png"
        if self.invincibility:
            pass
    
    def attack(self, enemies):
        if not self.attacking:
            self.attacking = True
            self.attack_counter=0
            #check ennemi touché ou départ d'un projectile

            if not self.weapon:
                attack_range = default_player_attack_range
                damages = default_player_damages
            else:
                attack_range = self.weapon.attack_range
                damages = self.weapon.damages
            

            if self.direction == "up":
                hit_rect = pygame.Rect(self.rect.centerx - 1, self.y - attack_range, 2, attack_range)
            elif self.direction == "down":
                hit_rect = pygame.Rect(self.rect.centerx - 1, self.rect.bottom, 2, attack_range)
            elif self.direction == "left":
                hit_rect = pygame.Rect(self.x - attack_range, self.surface.centery - 1, attack_range, 2)
            elif self.direction == "right":
                hit_rect = pygame.Rect(self.rect.right, self.surface.centery - 1, attack_range, 2)

            for enemy in enemies:
                if hit_rect.colliderect(enemy.rect):
                    enemy.hit(damages * self.strength_multiplier)
