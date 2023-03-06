from settings import *
from Entity.entity import *
from Utilities.debug import *

class Player(Entity):
    def __init__(self, x, y, groupes, collision_blocks):
        self.image = player_imgs["up"]["up_0.png"]
        super().__init__(x, y, self.image, groupes)
        self.rect = self.image.get_rect()
        self.surface = pygame.Rect(self.x, self.y, 64, 40) #à modif
        self.collision_blocks = collision_blocks
        self.basey = self.surface.centery
        self.direction = "down"
        self.animation_counter = 0
        

    def move(self, keys):
        """Déplacement et collisions du personnage principal

        Args:
            keys (list): Liste des touches pressées par le joueur
        """
        self.movement = pygame.math.Vector2()
        self.movement.x, self.movement.y = 0,0
        if keys[pygame.K_LEFT]:
            self.movement.x += -1
            self.direction = "left"
        if keys[pygame.K_RIGHT]:
            self.movement.x += 1
            self.direction = "right"
        if keys[pygame.K_UP]:
            self.movement.y += -1
            self.direction = "up"
        if keys[pygame.K_DOWN]:
            self.movement.y += 1
            self.direction = "down"

        if self.movement.length() != 0:
            self.movement = self.movement.normalize()
        
        if self.check_collision(self.collision_blocks, "horizontal", self.movement.x * playerspeed) == False:
            self.x += self.movement.x * playerspeed
            
        if self.check_collision(self.collision_blocks, "vertical", self.movement.y * playerspeed) == False:
            self.y += self.movement.y * playerspeed
            
        
        
        self.x = round(self.x)
        self.y = round(self.y)
        
        self.surface.topleft = (self.x,self.y)
        self.basey = self.surface.centery

    def update(self):
        if self.movement.length() == 0:
            self.image = player_imgs[self.direction+"_idle"]["idle_"+self.direction+".png"]
            self.animation_counter = 0
        else:
            self.image = player_imgs[self.direction][self.direction+"_"+str(self.animation_counter//walk_anim_duration)+".png"]
            self.animation_counter +=1
            if self.animation_counter >= walk_anim_duration * 4:
                self.animation_counter = 0
            


#    def draw(self, surface):
#        """Méthode : affiche le joueur à l'écran et gère les animations
#        """
#        #TODO ajouter animations
#        self.image = player_img
#        surface.blit(self.image, (self.x,self.y))
        