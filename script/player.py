from settings import *

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        

    def move(self, keys):
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
        self.x += self.movement.x * playerspeed
        self.y += self.movement.y * playerspeed

    def draw(self, surface):
        """Méthode : affiche le joueur à l'écran et gère les animations
        """
        self.image = player_img
        surface.blit(self.image, (self.x,self.y))
        