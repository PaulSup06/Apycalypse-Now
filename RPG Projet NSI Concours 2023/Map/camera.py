import pygame
from settings import *

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
        if player.surface.centerx >self.half_width:
            self.offset.x = player.surface.centerx - self.half_width
        else:
            self.offset.x = 0
        if player.surface.centery >self.half_height:
            self.offset.y = player.surface.centery - self.half_height
        else:
            self.offset.y = 0

        bg_offset_pos = self.bg_rect.topleft - self.offset
        self.screen.blit(self.bg_img, bg_offset_pos)

        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.basey):
            offset_pos = sprite.surface.topleft - self.offset
            self.screen.blit(sprite.image, offset_pos)

        #debug
        #for entity in self.collision_blocks:
        #    pygame.draw.rect(self.screen, "white", entity.surface, width=2)
        #pygame.draw.rect(self.screen, "white", self.player.surface, width=2)
        ##debug([self.player.movement.length(),self.player.x,self.player.y, len(self.level.visible_blocks.sprites())])
