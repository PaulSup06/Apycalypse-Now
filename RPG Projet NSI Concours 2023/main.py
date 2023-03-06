import pygame
from settings import *
from Map.level import Level
from Utilities.debug import debug
import sys
from Utilities.debug import *

class Game:
    def __init__(self):
        """initialisation générale
        """
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.font.init()
        pygame.display.set_caption("RPG") #ajouter titre du jeu ici
        pygame.display.set_icon(player_img) #TODO rajouter une petite icone sympa
        self.clock = pygame.time.Clock()
        self.running = True
        #génération du monde
        self.level = Level() 
        self.player = self.level.player
    
    def run(self):
        """Boucle de code principale
        """
        while self.running:
            self.screen.fill((0,0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    #TODO éventuellement sauvegarder ici
                    pygame.quit()
                    sys.exit()
            
            self.player.move(pygame.key.get_pressed())
            self.player.update()
            self.level.visible_blocks.draw_visible(self.player)

           
            debug(["FPS : " + str(self.clock.get_fps()), self.player.movement.length()])
            pygame.display.update()
            self.clock.tick(FPS)

#===============================================================
#====PROGRAMME PRINCIPAL========================================
#===============================================================

if __name__=='__main__':
    game = Game()  
    game.run()