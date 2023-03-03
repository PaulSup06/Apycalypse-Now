import pygame

def debug(datas):
    """Affiche une donnée en haut à gauche de l'écran dans le jeu 
    (plus facile d'utilisation que la console si plusieurs variables à affocher)

    Args:
        data (List): données à afficher dans le debug
        surface (pygame.surface): surface sur laquelle afficher le debug
    """
    surface = pygame.display.get_surface()
    font = pygame.font.Font(None,30)
    for i, data in enumerate(datas):
        rendered_font = font.render(str(data),True,"white")
        surface.blit(rendered_font,(10,10 + i*20))