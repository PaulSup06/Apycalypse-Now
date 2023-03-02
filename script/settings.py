import pygame
import os

#Paramètres généraux
WIDTH = 1250
HEIGHT = 700
FPS = 60


#variables de gameplay
playerspeed = 5

#textures
#TODO ajouter et modifier système de load d'images 
#(à faire éventuellement en continue pour le cas des animations ?)
#player_img = {"bas":pygame.image.load(os.path.join("textures","player","down","down_0.png"))}
player_img = pygame.image.load("textures\\test\\player.png")
rock_img = pygame.image.load(os.path.join("textures","test","rock.png"))