from settings import * 
from case import Case
from debug import debug
from camera import Camera
from player import *

class Level:
    def __init__(self, level=0) -> None:
        """Génération d'un niveau et affichage à l'écran
        Args:
            level (int): niveau à générer (par défaut 0 = debug)
        """
        
        self.visible_blocks = Camera(level)
        self.collision_blocks = pygame.sprite.Group() 
        if level == 0:
            self.world = test_world
        for row_num, row in enumerate(self.world):
            for col_num, col in enumerate(row):
                if col==1:
                    Case(col_num*CASE_SIZE, row_num*CASE_SIZE, [self.collision_blocks, self.visible_blocks], rock_img)
                if col==2:
                    self.player = Player(int(col_num*CASE_SIZE), int(row_num*CASE_SIZE), self.visible_blocks, self.collision_blocks)
        


