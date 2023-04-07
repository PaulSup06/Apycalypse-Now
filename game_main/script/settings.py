import pygame
import os
import time
import csv

#Paramètres généraux
WIDTH = 1280
HEIGHT = 720
FPS = 60
CASE_SIZE = 64
GAME_TITLE = 'RPG NSI'

#inventaire
GRID_SIZE = 5
GRID_OFFSET_X = 32
GRID_OFFSET_Y = 64
CELL_MARGIN = 4
CURSOR_COLOR = (255, 255, 0)

MAX_ITEMS_PER_CELL = 64
BACKGROUND_COLOR = (0, 0, 0)
ITEM_SIZE = (32,32)

#folders et paths
music_folder = "..\\audio"
sound_folder = "..\\sound"
settings_path ="..\\misc\\settings.csv"
default_settings_path ="..\\misc\\default_settings.csv"

#settings handling
settings_fields = ["k_up","k_down","k_right","k_left","k_attack","k_interact","k_escape","k_inventory","volume"]
settings_name = {'volume': 'Volume musique :',
                 'k_up': 'Haut : ',
                 'k_down': 'Bas : ',
                 'k_right': 'Droite : ',
                 'k_left': 'Gauche : ',
                 'k_attack': 'Attaquer :',
                 'k_interact': 'Interagir : ',
                 'k_inventory': "Ouvrir l'inventaire : ",
                 'k_escape': 'Sortir : '}

def get_actual_settings():
    with open(settings_path, newline="") as f:
        settings = csv.DictReader(f)
        actual_settings = {}
        for line in settings:
            for field in settings_fields:
                actual_settings[field] = line[field]
            
    return actual_settings


#variables de gameplay
playerspeed = 5
hitbox_offset = 15 #marge pour les collisions du joueur
walk_anim_duration = 12 #nombre de frames que dure 1 image de l'animation de marche
default_player_life = 6
default_player_attack_cooldown = 20 #cooldown par défaut quand main vide
default_player_attack_range = 32 #nombre de pixels du range de l'attaque avec les mains vides
default_player_damages = 2
enemy_anim_duration = 8 #nombre de frames pour chaque image de l'animation des enemies 
distance_affichage_npc_prompt = 300
interact_distance = 100
dialog_cooldown = 2 #nombre de frames entre l'affichage de chaque caractère du dialogue
door_unlock_range = 3*CASE_SIZE
stackable_range = 100
enemy_caracteristics = {
                        "bamboo":{
                            "speed":5,
                            "damages":1,
                            "health":3,
                            "drops":[
                                {
                                    "name":"life_potion",
                                    "drop_rate":50,
                                    "drop_count":1,                                    
                                }, {
                                    "name":"speed_potion",
                                    "drop_rate":50,
                                    "drop_count":1,                                    
                                }
                            ]
                        }
                       }

spike_exit_speed = 17
spike_damage = 1

# variable potion
speed_potion_duration = 15 # en seconde
speed_potion_mutltiplier = 1.5 

strength_potion_duration = 15 # en seconde
strength_potion_mutltiplier = 2.5 

invincibility_potion_duration = 5 # en seconde

#textures
player_img_folder = "..\\textures\\player"
enemy_img_folder = "..\\textures\\enemies"
spike_img_folder = "..\\textures\\spike"
misc_folder = "..\\textures\\misc"
items_folder="..\\textures\\items"
def load_imgs():
    """Charge les textures principales du jeu (appellée après initialisation vidéo pygame car convertion)
    """
    #textures joueur
    player_imgs = load_player_imgs()
    #textures mobs
    #textures NPC
    return player_imgs

def load_player_imgs():
    """Charge les images du joueur dans un dict de dict 
    ex : {"up":{"up_0.png":image,
                "up_1.png":image,
                "up_2.png":image},
        "down":{...}}

    Returns:
        dict: dict de dict contenant toutes les images des animations du joueur
    """ 
    
    player_imgs = {}
    for folder in os.listdir(player_img_folder):
        player_imgs[folder] = {}
        for file in os.listdir(os.path.join(player_img_folder, folder)):
            player_imgs[folder][file] = pygame.image.load(os.path.join(player_img_folder,folder,file)).convert_alpha()
    return player_imgs

def load_enemy_imgs():
    enemy_imgs = {}
    for type in os.listdir(enemy_img_folder):
        enemy_imgs[type] = {}
        for folder in os.listdir(os.path.join(enemy_img_folder, type)):
           enemy_imgs[type][folder] = []
           for file in os.listdir(os.path.join(enemy_img_folder,type,folder)):
               enemy_imgs[type][folder].append(pygame.image.load(os.path.join(enemy_img_folder,type,folder,file)).convert_alpha())
               
    return enemy_imgs

def load_spike_imgs():
    spike_imgs = []

    for file in os.listdir(os.path.join(spike_img_folder)):
        spike_imgs.append(pygame.image.load(os.path.join(spike_img_folder,file)).convert_alpha())
            
    return spike_imgs

def load_door_imgs():
    door_imgs = []
    for i in range(5):
        door_imgs.append(pygame.image.load(os.path.join(misc_folder,f"door{i}.png")).convert_alpha())
    
    return door_imgs

def load_item_imgs():
    item_images = {}
    for file_name in os.listdir(items_folder):
        item_name = os.path.splitext(file_name)[0]
        item_images[item_name] = pygame.image.load(os.path.join(items_folder, file_name))

    return item_images

def load_terminal_img():
    """Possibilité de rajouter une animation si besoin 
    """
    return pygame.image.load(os.path.join(misc_folder,"terminal.png")).convert()

#HTML
def load_html(id):
    """Charge un fichier html en string pour l'affichage avec pywebview

    Args:
        id (int): id du terminal/du site à afficher

    Returns:
        str: html décodé du fichier
    """
    with open(f"..\\web\\body_terminal{id}.html", encoding="utf-8") as f:
      
        return f.read()
#fonts
pygame.font.init()
font1 = pygame.font.SysFont("sans-serif",30)
font2 = pygame.font.SysFont("sans-serif",23)
title_font = pygame.font.SysFont("Arial",60, True)
button_font = pygame.font.SysFont("Arial",35, True)


#dialogues
npc_dialogs = {
    "John":{
        
            "1":{
                    "type": "sans_choix",
                    'text':'Bonjour aventurier ! Je ne vous avais jamais vu dans les parages auparavant...',
                    "goto": "2",
                    "npc_update":["True","...","2"],
                },
            "2":{
                    "type": "sans_choix",
                    'text':"Vous voulez aller vers l'Est ? Je ne m'y risquerais pas... \n J'ai entendu de terribles histoires sur cet endroit depuis la grande catastrophe",
                    "goto": "-1",
                    "npc_update":["True","...","3"],
                },
            "3":{
                    "type": "avec_choix",
                    "text":"Une question avec un choix",
                    "choix":[
                        {"index":1,
                        "text": "choix1",
                        "goto":"1",
                        "npc_update":["True","...","1"],
                        },
                        {"index":2,
                        "text": "choix2",
                        "goto":"4",
                        "npc_update":["True","...","4"],
                        },
                        {"index":3,
                        "text": "choix3",
                        "goto":"2",
                        "npc_update":["True","...","1"],
                        },
                        {"index":4,
                        "text": "choix4",
                        "goto":"4",
                        "npc_update":["True","...","4"],
                        }
                    ]
                },
            "4":{
                "type": "sans_choix",
                "text":"un dialogue qui se ferme sans rien faire",
                "goto": "-1",
                "npc_update":["True","...","1"],
            }
        }
    }

#misc
button_fillcolors = {'normal': (0,0,0,0),
                     'hover': (0,0,0,100),
                     'pressed': (140,140,140,140),
                     'text':(255,255,255)}

item_names_render = {
    "life_potion":"Potion de soin",
    "speed_potion":"Potion de vitesse",
    "strength_potion":"Potion de force",
    "invincibility_potion":"Potion d'invincibilité",
}
#temp
#test_world = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
#         [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
#         [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
#         [1,0,0,2,0,0,0,0,0,0,0,0,0,0,1],
#         [1,0,0,1,0,0,0,0,0,0,0,0,0,0,1],
#         [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
#         [1,1,1,1,1,1,1,1,0,1,1,1,1,1,1],]
showing_hitbox=False