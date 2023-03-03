from settings import *

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = None
        self.hitbox = pygame.Rect(self.x, self.y + 12, 64, 40) #à modif
        

    def move(self, keys):
        """Déplacement et collisions du personnage principal

        Args:
            keys (list): Liste des touches pressées par le joueur
        """
        self.movement = pygame.math.Vector2()
        if keys[pygame.K_LEFT]:
            self.movement.x = -1
        if keys[pygame.K_RIGHT]:
            self.movement.x = 1
        if keys[pygame.K_UP]:
            self.movement.y = -1
        if keys[pygame.K_DOWN]:
            self.movement.y = 1

        if self.movement.length() != 0:
            self.movement = self.movement.normalize()
        
        #TODO collisions
        self.x += self.movement.x * playerspeed
        self.y += self.movement.y * playerspeed

    def draw(self, surface):
        """Méthode : affiche le joueur à l'écran et gère les animations
        """
        #TODO ajouter animations
        self.image = player_img
        surface.blit(self.image, (self.x,self.y))
        