from settings import * 
from player import Player

class Level:
    def __init__(self, level=0) -> None:
        """Génération d'un niveau et affichage à l'écran
        """
        self.player = Player(200,200)