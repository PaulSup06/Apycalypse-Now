from settings import * 
from player import Player
from case import Case
from debug import *

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
                    self.player = Player(int(col_num*CASE_SIZE), int(row_num*CASE_SIZE))
        


class Camera(pygame.sprite.Group):
    def __init__(self, world):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.bg_img = world_bg[world]

    def draw_visible(self):   
        self.screen.blit(self.bg_img, (0,0))
        for sprite in self.sprites():
            pos = sprite.surface.topleft
            self.screen.blit(sprite.image, pos)
