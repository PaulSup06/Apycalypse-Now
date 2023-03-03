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
                    self.player = Player(int(col_num*CASE_SIZE), int(row_num*CASE_SIZE), self.visible_blocks, self.collision_blocks)
        


class Camera(pygame.sprite.Group):
    def __init__(self, world):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.half_width = self.screen.get_size()[0] // 2
        self.half_height = self.screen.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        self.bg_img = world_bg[world].convert()
        self.bg_rect = self.bg_img.get_rect(topleft = (0,0))

    def draw_visible(self, player):   

        #calcul de l'offset pour garder le joueur au centre
        self.offset.x = player.surface.centerx - self.half_width
        self.offset.y = player.surface.centery - self.half_height

        bg_offset_pos = self.bg_rect.topleft - self.offset
        self.screen.blit(self.bg_img, bg_offset_pos)

        for sprite in self.sprites():
            offset_pos = sprite.surface.topleft - self.offset
            self.screen.blit(sprite.image, offset_pos)

         #debug
        #for entite in self.collision_blocks:
        #    pygame.draw.rect(self.screen, "white", entite.surface, width=2)
        #pygame.draw.rect(self.screen, "white", self.player.surface, width=2)
        ##debug([self.player.movement.length(),self.player.x,self.player.y, len(self.level.visible_blocks.sprites())])
