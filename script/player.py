from settings import *
from entite import Entite
from debug import *

class Player(Entite):
    def __init__(self, x, y, groupes, collision_blocks):
        self.image = player_img
        super().__init__(x, y, self.image, groupes)
        self.rect = self.image.get_rect()
        self.surface = pygame.Rect(self.x, self.y, 64, 40) #à modif
        self.collision_blocks = collision_blocks
        

    def move(self, keys):
        """Déplacement et collisions du personnage principal

        Args:
            keys (list): Liste des touches pressées par le joueur
        """
        self.movement = pygame.math.Vector2()
        self.movement.x, self.movement.y = 0,0
        if keys[pygame.K_LEFT]:
            self.movement.x += -1
        if keys[pygame.K_RIGHT]:
            self.movement.x += 1
        if keys[pygame.K_UP]:
            self.movement.y += -1
        if keys[pygame.K_DOWN]:
            self.movement.y += 1

        if self.movement.length() != 0:
            self.movement = self.movement.normalize()
        
        #TODO collisions
        if self.check_collision(self.collision_blocks, "horizontal", self.movement.x * playerspeed) == False:
            self.x += self.movement.x * playerspeed
            debug(["False"])
        else:
            debug(["True"])
        if self.check_collision(self.collision_blocks, "vertical", self.movement.y * playerspeed) == False:
            self.y += self.movement.y * playerspeed
            debug(["False"])
        else:
            debug(["True"])
        
        self.x = round(self.x)
        self.y = round(self.y)
        
        self.surface.topleft = (self.x,self.y)

#    def draw(self, surface):
#        """Méthode : affiche le joueur à l'écran et gère les animations
#        """
#        #TODO ajouter animations
#        self.image = player_img
#        surface.blit(self.image, (self.x,self.y))
        