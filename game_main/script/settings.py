import pygame
import os
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
ITEM_SIZE = (45,45)


#son
actual_sound_channel = 1

#folders et paths
music_folder = "..\\audio"
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
hitbox_offset = 30 #marge pour les collisions du joueur
walk_anim_duration = 12 #nombre de frames que dure 1 image de l'animation de marche
default_player_life = 6
default_player_attack_cooldown = 20 #cooldown par défaut quand main vide
default_player_attack_range = 40 #nombre de pixels du range de l'attaque avec les mains vides
default_player_damages = 2
enemy_anim_duration = 15 #nombre de frames pour chaque image de l'animation des enemies 
distance_affichage_npc_prompt = 300
interact_distance = 110
dialog_cooldown = 2 #nombre de frames entre l'affichage de chaque caractère du dialogue
door_unlock_range = 3*CASE_SIZE
stackable_range = 100
enemy_drops = {
                "bamboo":[
                        {
                            "name":"life_potion",
                            "drop_rate":40,
                            "drop_count":1,                                    
                        }, {
                            "name":"speed_potion",
                            "drop_rate":30,
                            "drop_count":1,                                    
                        }
                    ],
                "vampire":[
                        {
                            "name":"life_potion",
                            "drop_rate":25,
                            "drop_count":2,                                    
                        }, {
                            "name":"invincibility_potion",
                            "drop_rate":10,
                            "drop_count":1,                                    
                        },{
                            "name":"strength_potion",
                            "drop_rate":45,
                            "drop_count":1,                                    
                        }
                    ], 
                "zombie":[
                    {
                            "name":"life_potion",
                            "drop_rate":15,
                            "drop_count":1,                                    
                        },{
                            "name":"strength_potion",
                            "drop_rate":25,
                            "drop_count":1,                                    
                        }
                ],
                "tronc":[
                    {
                            "name":"life_potion",
                            "drop_rate":10,
                            "drop_count":1,                                    
                        },
                ]
                }
                       

spike_exit_speed = 17
spike_damage = 1

# variable potion
speed_potion_duration = 15 # en seconde
speed_potion_multiplier = 1.5 

strength_potion_duration = 15 # en seconde
strength_potion_mutltiplier = 2.5 

invincibility_potion_duration = 5 # en seconde

#ui
pick_up_notification_duration = 2 #sec
bloodscreen_show_time = 3

#textures
player_img_folder = "..\\textures\\player"
enemy_img_folder = "..\\textures\\enemies"
spike_img_folder = "..\\textures\\spike"
lever_img_folder = "..\\textures\\lever"
misc_folder = "..\\textures\\misc"
items_folder="..\\textures\\items"
npc_img_folder = "..\\textures\\npc"

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
            
            base_img = pygame.image.load(os.path.join(player_img_folder,folder,file)).convert_alpha()
            rect = base_img.get_bounding_rect()
            #supposons que l'image est centrée et avec la base en bas
            img_cropped = base_img.subsurface(pygame.Rect((base_img.get_width()-rect.width)//2, base_img.get_height() - rect.height, rect.width, rect.height))
            player_imgs[folder][file] = pygame.transform.scale(img_cropped,(rect.width*4, rect.height*4))
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

def load_switches_imgs():

    files = os.listdir(os.path.join(lever_img_folder))
    # floor_lever1
    imgs={
        "floor_lever1" : [pygame.image.load(os.path.join(lever_img_folder,file)).convert_alpha() for file in files if file == "01.png" or  file == "13.png" or file == "25.png" or  file == "37.png"],
        "floor_lever2" : [pygame.image.load(os.path.join(lever_img_folder,file)).convert_alpha() for file in files if file == "04.png" or  file == "16.png" or file == "28.png" or  file == "40.png"],
        "floor_lever3" : [pygame.image.load(os.path.join(lever_img_folder,file)).convert_alpha() for file in files if file == "10.png" or  file == "22.png" or file == "34.png"],
        "manivelle" : [pygame.image.load(os.path.join(lever_img_folder,file)).convert_alpha() for file in files if file == "44.png" or  file == "08.png" or file == "20.png"or file == "32.png"],
        "wall_lever" : [pygame.image.load(os.path.join(lever_img_folder,file)).convert_alpha() for file in files if file == "00.png" or  file == "12.png" or file == "24.png"or file == "36.png"],
        "pressure_plate1" : [pygame.image.load(os.path.join(lever_img_folder,file)).convert_alpha() for file in files if file == "50.png" or  file == "62.png" or file == "74.png"or file == "86.png"],
        "pressure_plate2" : [pygame.image.load(os.path.join(lever_img_folder,file)).convert_alpha() for file in files if file == "48.png" or  file == "60.png" or file == "72.png"or file == "84.png"],
        "pressure_plate3" : [pygame.image.load(os.path.join(lever_img_folder,file)).convert_alpha() for file in files if file == "53.png" or  file == "65.png" or file == "77.png"or file == "89.png"],
    }
    
            
    return imgs

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
    #TURTLEDOVE A MODIFIER
    "Osborn Turtledove":{
        
            "1":{
                    "type": "avec_choix",
                    'text':'Vous êtes Nils je suppose... on m\'a parlé de votre arrivée.',
                    "choix":[
                        {"index":1,
                        "text": "Oui, c'est moi",
                        "goto":"2",
                        "npc_update":[True,"...","1"],
                        },
                        {"index":2,
                        "text": "Qui vous a parlé de moi ?",
                        "goto":"3",
                        "npc_update":[True,"...","3"],
                        }
                    ]
                },
            "2":{
                    "type": "avec_choix",
                    'text':"Comme vous le savez sûrement, l'humanité est depuis peu sous menace d'extinction.\nLe Cristal de Feu a été brisé, hélas!",
                    "choix":[
                        {"index":1,
                        "text": "Qu'est-ce que le \"Cristal de Feu\"?..",
                        "goto":"4",
                        "npc_update":[True,"...","4"],
                        },
                        {"index":2,
                        "text": "J'ai entendu, c'est pour ça que je suis ici",
                        "goto":"5",
                        "npc_update":[True,"...","5"],
                        }
                    ]
                },
            "3":{
                    "type": "avec_choix",
                    "text":"Un ancien moine du temple m'a donné une lettre il y a peu. Votre nom y figuré. \nTenez, je vous la met dans votre sac.",
                    "choix":[
                        {"index":1,
                        "text": "Merci",
                        "goto":"2",
                        "npc_update":[True,"...","2"],
                        }
                    ]
                },
            "4":{
                "type": "sans_choix",
                "text":"Le Cristal de Feu est une pierre dont la forme est parfaite. Jamais l'humanité a-t-elle pu reproduire une telle perfection. ",
                "goto": "5",
                "npc_update":[True,"...","5"],
            },
            "5":{
                "type": "sans_choix",
                "text":"D'après une légende ancienne, le jour où ce cristal se brisera, la Terre connaîtra son trépas, \npollution et destruction règneront en maîtres, et l'humanité en paiera les êtres.",
                "goto": "6",
                "npc_update":[True,"...","6"],
            },
            "6":{
                "type": "avec_choix",
                "text":"Quelle misère! Le temps nous est compté! Voudrais-tu bien nous aider dans notre quêtre ?",
                "choix":[
                    {"index":1,
                    "text": "Oui! Allons sauver la terre!",
                    "goto":"-1",
                    "npc_update":[True,"...","7"],
                    "add_item":("note#2",1)
                    }
                ]
            },
            "7":{
                "type": "sans_choix",
                "text":"Allons, pas de temps à perdre ! Fonce !",
                "goto": "-1",
                "npc_update":[True,"...","7"],
                }
        },
    
    #==============================================================================================================================================================================
    #SOLDAT PNJ DE TUTORIEL
    #==============================================================================================================================================================================
    
    "soldier":{
        "1":{
            "type": "sans_choix",
                "text":"Bonjour ! Te voilà enfin réveillé ! ",
                "goto": "2",
                "npc_update":[True,"...","2"],
        },
        "2":{
                "type": "avec_choix",
                "text":"Tu as dormi pendant très longtemps ! Te souviens-tu de ce qui t'es arrivé ?",
                "choix":[
                    {"index":1,
                    "text": "Oui! (passer tutoriel)",
                    "goto":"-1",
                    "npc_update":[True,"...","10"],
                    },
                    {"index":2,
                    "text": "Vaguement... (aller à l'histoire)",
                    "goto":"6",
                    "npc_update":[True,"...","6"],
                    },
                    {"index":3,
                    "text": "Non... (tutoriel de base)",
                    "goto":"3",
                    "npc_update":[True,"...","3"],
                    }
                ]
            },
        #TUTORIEL DE BASE
        "3":{
            "type": "sans_choix",
            "text":"Très bien... Je suppose que tu as dû te cogner suffisamment fort pour oublier tout cela...\nQuoi qu'il en soit reprenons du début.\nTu peux utiliser la touche ECHAP de ton clavier pour accéder au menu de pause.\nDe là, accède au menu des paramètres. Tu y trouveras les touches importantes.",
            "goto": "4",
            "npc_update":[True,"...","4"],},
        "4":{
            "type": "sans_choix",
            "text":"Ensuite, de ce même menu de pause, tu pourras sauvegarder la partie.\nTu retrouveras tes sauvegardes depuis le menu principal.\nAttention ! Toute progression non sauvegardée sera perdue.",
            "goto": "5",
            "npc_update":[True,"...","5"],},
        "5":{
            "type": "sans_choix",
            "text":"Dans le cas très improbable où tu viendrais à mourir, ne t'inquiète pas tu as la possibilité de te réanimer.\nCependant si comme nous tu es un puriste, tu peux toujours recommencer à ta dernière sauvegarde ou du début !",
            "goto": "6",
            "npc_update":[True,"...","6"],},
        
        #HISTOIRE
        "6":{
            "type": "avec_choix",
            "text":"Bien... Je suppose que je vais maintenant devoir te raconter l'histoire de la catastrophe...",
            "choix":[
                {"index":1,
                "text": "La catastrophe ?",
                "goto":"7",
                "npc_update":[True,"...","7"],
                },
                {"index":2,
                "text": "Non merci, je suis au courant",
                "goto":"10",
                "npc_update":[True,"...","10"],
                }
                
            ]
        },
        "7":{
            "type": "sans_choix",
            "text":"Tout a démarré il y a quelques années, lorsque ce docteur, Osborn Turtledove, s'est mis en tête de sauver l'humanité...\nLa crise et les pénuries grandissant, il a développé une molécule qui, introduite dans les sources d'énergies fossiles\n (gaz, pétrole, ...) aurait selont lui permis de diviser par 100 la consommation énergétique du monde.",
            "goto": "8",
            "npc_update":[True,"...","8"],},
        "8":{
            "type": "sans_choix",
            "text":"Tout d'abord, personne ne s'est rendu compte de rien, le produit produisait l'effet escompté\n et le docteur Turledove était porté en héros dans le monde entier.\nMais après quelques mois, son produit répandu partout se révéla être toxique.",
            "goto": "15",
            "npc_update":[True,"...","15"],},
        "15":{
            "type": "sans_choix",
            "text":"Les êtres vivants les plus exposés commencèrent à tomber malade...\nIls agirent de manière étrange, attaquant sans raison apparente leurs congénères.\nLes humains ne furent pas épargnés, et le monde sombra dans le chaos.",
            "goto": "9",
            "npc_update":[True,"...","9"],},
        "9":{
            "type": "sans_choix",
            "text":"Depuis, de nombreuses personnes essayent d'accéder à son laboratoire afin de trouver un antidote,\n mais personne n'a pour l'instant réussi.\nC'est à l'entrée de celui-ci que je t'ai trouvé, tu dois surement être un autre aventurier...\nPeu m'importe, vas donc remplir ta mission, que je ne t'aie pas sauvé pour rien !",
            "goto": "10",
            "npc_update":[True,"...","10"],},
        "10":{
            "type": "avec_choix",
            "text":"Bien... As-tu des questions ?",
            "choix":[
                {"index":1,
                "text": "On parle bien de zombies là ??",
                "goto":"11",
                "npc_update":[True,"...","10"],
                },
                {"index":2,
                "text": "Où dois-je aller ?",
                "goto":"12",
                "npc_update":[True,"...","10"],
                },
                {"index":3,
                "text": "Non",
                "goto":"-1",
                "npc_update":[True,"...","10"],
                }
                
            ]
        },
        "11":{"type": "sans_choix",
            "text":"Certaines personnes ont employé ces mots, mais leur comportement n'est pas le même.\nIls attaquent pour tuer et non pour contaminer ou pour se nourrir. De plus, personne n'a réussi\nà déterminer la cause réelle de ce phénomène, ni à identifier un quelconque virus ou parasite.",
            "goto": "10",
            "npc_update":[True,"...","10"],},
        "12":{"type": "sans_choix",
            "text":"Le laboratoire de Turtledove se trouve plus au nord,\nnous avons trouvé il y a quelques mois une entrée cachée par ce chateau en ruines, \nmais personne depuis n'a réussi à franchir les portes blindées qui en gardent l'entrée souterraine.",
            "goto": "10",
            "npc_update":[True,"...","10"],},
    },

    #==============================================================================================================================================================================
    #WOODBARON, PNJ ENTREE CHATEAU
    #==============================================================================================================================================================================
    
    "Reimond Woodbaron":{
            
                "1":{
                        "type": "sans_choix",
                        'text':"Ah! Voilà quelqu'un... Je croyais pourtant être seul dans ce désert... ",
                        "goto": "2",
                        "npc_update":[True,"...","2"],
                    },
                "2":{
                        "type": "avec_choix",
                        'text':"Mais qui peut-il bien être... Mystère.",
                        "choix":[
                            {"index":1,
                            "text": "Je vous retourne la question",
                            "goto":"3",
                            "npc_update":[True,"...","4"],
                            },
                            {"index":2,
                            "text": "Je viens accomplir une mission",
                            "goto":"3",
                            "npc_update":[True,"...","3"],
                            }
                        ]
                    },
                "3":{
                        "type": "avec_choix",
                        "text":"Il parle en plus ? Mais a qui... À moi ?\nEnfin, à qui d'autre pourrais-il parler ici...",
                        "choix":[
                            {"index":1,
                            "text": "Je cherche quelque chose ici",
                            "goto":"4",
                            "npc_update":[True,"...","4"],
                            },],
                        
                    },
                "4":{
                    "type": "sans_choix",
                    "text":"Il cherche quelque chose ?\n Enfin, tout le monde sait que rien ne vit ici à part des infectés !\n M'enfin, s'il peut m'aider à rentrer, je ne dirais pas non...",
                    "goto": "6",
                    "npc_update":[True,"...","6"],
                },

                "6":{
                    "type": "avec_choix",
                    "text":"Mais pour cela, je dois trouver la manivelle permettant d'actionner la herse du château.\nOui, c'est ça, une manivelle. Peut-être sait-il comment la trouver ?",
                    "choix":[
                        {"index":1,
                        "text": "Eh oh, je suis là...",
                        "goto":"7",
                        "npc_update":[True,"...","7"],
                        }
                    ]
                },
                "7":{
                    "type": "sans_choix",
                    "text":"Bon... Je vais lui donner ma carte, il saura surement mieux la déchiffrer que moi...",
                    "goto": "8",
                    "npc_update":[True,"...","8"],
                    "add_item":("note#1",1)
                },
                "8":{
                    "type": "avec_choix",
                    "text":"...",
                    "choix":[
                        {"index":1,
                        "text": "Mais où dois-je aller ?",
                        "goto":"9",
                        "npc_update":[True,"...","9"],
                        },
                        {"index":2,
                        "text": "Je n'y comprends rien...",
                        "goto":"9",
                        "npc_update":[True,"...","9"],
                        },
                        {"index":3,
                        "text": "Au revoir",
                        "goto":"-1",
                        "npc_update":[True,"...","9"],
                        }
                        
                    ]
                },
                "9":{
                    "type": "sans_choix",
                    "text":"...",
                    "goto": "-1",
                    "npc_update":[False,"La fin est proche...","9"],
                },
            },
        
    
}



#misc
button_fillcolors = {'normal': (0,0,0,0),
                     'hover': (0,0,0,100),
                     'pressed': (140,140,140,140),
                     'text':(255,255,255)}

def convert_to_tuple(value):
    """Convertit les arguments des triggers en tuple exploitable

    Args:
        value (str): argument tiled des triggers

    Returns:
        tuple: arguments du trigger
    """
    if value[0]=='(':
        value = value[1:]
    if value[-1]==')':
        value = value[:-1]
    result = []
    for row in value.split('),('):
        row_tup = []
        for field in (f.strip() for f in row.split(',')):
            if (field[0]=="'"and field[-1]=="'") or (field[0]=='"' and field[-1]=='"'):
                row_tup.append(field[1:-1])
            else:
                row_tup.append(field)
        if len(row_tup)==1:
            result.append(row_tup[0])
        else:
            result.append(tuple(row_tup))

    return tuple(result)

item_names_render = {
    "life_potion":"Potion de soin",
    "speed_potion":"Potion de vitesse",
    "manivelle":"Manivelle",
    "strength_potion":"Potion de force",
    "pelle":"Pelle",
    "note":"Note",
    "note#1":"Carte",
    "invincibility_potion":"Potion d'invincibilité",
}

showing_hitbox=False

