from settings import * 
from player import Player
from case import Case

class Level:
    def __init__(self, level=0) -> None:
        """Génération d'un niveau et affichage à l'écran
        Args:
            level (int): niveau à générer (par défaut 0 = debug)
        """
        self.player = Player(200,200)
        self.visible_blocks = Camera()
        self.collision_blocks = pygame.sprite.Group() 
        if level == 0:
            self.world = test_world
        for row in self.world:
            for col in row:
                if col==1:
                    Case(col*CASE_SIZE, row*CASE_SIZE, [self.collision_blocks, self.visible_blocks], rock_img)
        


class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()
        
    
