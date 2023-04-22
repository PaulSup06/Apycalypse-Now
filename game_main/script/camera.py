import pygame
from settings import *

class Camera(pygame.sprite.Group):
    def __init__(self, world):
        """Objet caméra : affiche les objets visibles à l'écran et calcule leur offset pour garder le joueur au centre. Hérite de pygame.sprite.Group car contient les éléments (sprites) à afficher.

        Args:
            world (int): id du monde en cours (affichage de l'arrière plan)
        """
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.half_width = self.screen.get_size()[0] // 2
        self.half_height = self.screen.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        self.bg_img = pygame.image.load(f"..\\worlds\\world{world}.png").convert()
        self.bg_rect = self.bg_img.get_rect(topleft = (0,0))

    #FONCTIONS UTILITAIRES (au cas où)
    #==============================================================
    def get_visible_blocks(self):
        """Renvoie les sprites visibles

        Returns:
            List (pygame.sprite.Sprite): liste contenant tout les éléments affichables
        """
        return self.sprites()
    
    def add_to_visible(self, element):
        """Ajoute un élément à afficher à l'écran

        Args:
            element (pygame.sprite): Sprite à afficher à l'écran
        """
        self.add(element)

    def remove_from_visible(self,element):
        """Retire un élément des sprites affichés à l'écran

        Args:
            element (pygame.sprite): Sprite à retirer
        """
        if self.has(element):
            self.remove(element)
            return element
        else:
            return None 
    #=======================================================================

    def draw_visible(self, player,npcs, enemies, tilemap, settings):   
        """Affiche les éléments à l'écran en fonction de la position du joueur

        Args:
            player (Player): objet du joueur pour sa position
        """
        #calcul de l'offset pour garder le joueur au centre
        if player.surface.centerx < self.half_width:
            self.offset.x = 0
        elif player.surface.centerx > tilemap.width * CASE_SIZE - self.half_width:
            self.offset.x = tilemap.width * CASE_SIZE - WIDTH
        else:
            self.offset.x = player.surface.centerx - self.half_width
            
        if player.surface.centery < self.half_height:
            self.offset.y = 0
        elif player.surface.centery > tilemap.height * CASE_SIZE - self.half_height:
            self.offset.y = tilemap.height * CASE_SIZE - HEIGHT
        else:
            self.offset.y = player.surface.centery - self.half_height

        bg_offset_pos = self.bg_rect.topleft - self.offset
        self.screen.blit(self.bg_img, bg_offset_pos)

        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.basey):
            offset_pos = (sprite.x,sprite.y) - self.offset
            self.screen.blit(sprite.image, offset_pos)

        # affichage de la barre de vie des ennemies
        for enemy in enemies:
            offset_pos = (enemy.x,enemy.y) - self.offset
            health_bar_width = 88
            pygame.draw.rect(self.screen, (0,0,0), (offset_pos.x -12, offset_pos.y -15, health_bar_width + 2, 9))
            pygame.draw.rect(self.screen, (255,255,255), (offset_pos.x -10, offset_pos.y - 13, health_bar_width, 6))
            # vie restante
            health = (enemy.health / enemy.max_health) * health_bar_width
            pygame.draw.rect(self.screen, (128,0,0), (offset_pos.x -10, offset_pos.y - 13, health, 6))
        
        for npc in npcs:
            if npc.check_distance_to([player.x,player.y],distance_affichage_npc_prompt):  
                npc.show_indicator(self.screen, self.offset, settings, player)  

                