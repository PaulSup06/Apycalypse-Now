import pygame
import os

#Paramètres généraux
WIDTH = 1250
HEIGHT = 700
FPS = 60
CASE_SIZE = 64


#variables de gameplay
playerspeed = 5
hitbox_margin = 0 #marge pour les collisions
walk_anim_duration = 12 #nombre de frames que dure 1 image de l'animation de marche

#textures
#TODO ajouter et modifier système de load d'images 
#(à faire éventuellement en continue pour le cas des animations ?)

player_img = pygame.image.load("game_main\\textures\\test\\player.png")

rock_img = pygame.image.load(os.path.join("game_main\\textures","test","rock.png"))
world_bg = {0:pygame.image.load("game_main\\textures\\test\\essai carte1.png")}

player_img_folder = "game_main\\textures\\player"

def load_player_imgs():
    """Charge les images du joueur dans un dict de dict 
    ex : {"up":{"up_0.png":image,
                "up_1.png":image,
                "up_2.png":image}
        "down":{...}}

    Returns:
        dict: dict de dict contenant toutes les images des animations du joueur
    """ 
    player_imgs = {}
    for folder in os.listdir(player_img_folder):
        player_imgs[folder] = {}
        for file in os.listdir(os.path.join(player_img_folder, folder)):
            player_imgs[folder][file] = pygame.image.load(os.path.join(player_img_folder,folder,file))
    return player_imgs

player_imgs = load_player_imgs()
#temp
test_world = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
         [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
         [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
         [1,0,0,2,0,0,0,0,0,0,0,0,0,0,1],
         [1,0,0,1,0,0,0,0,0,0,0,0,0,0,1],
         [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
         [1,1,1,1,1,1,1,1,0,1,1,1,1,1,1],]
