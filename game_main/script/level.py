from switch import Lever, Manivelle, PressurePlate
from settings import * 
from case import Case,Trigger
from debug import debug
from camera import Camera
from player import *
from npc import Npc, Door
from enemy import Enemy
from spike import Spike
from ui import Button
from browser import Terminal
import pytmx
import pygame
import os
import csv
import ast

class Level:
    def __init__(self, game, player_life, player_max_life, world=0,player_gen=True) -> None:
        """Génération d'un niveau et affichage à l'écran
        Args:
            game (Game): objet Game principal pour accéder à certaines méthodes et fonctions
            world (int): niveau à générer (par défaut 0 = debug)
            player_gen(Bool): True si le joueur est généré par le niveau, 
                sinon géré directement dans la class Game (ex : lors d'un chargement de sauvegarde).
                default = True
        """
        
        self.game = game #objet main pour les méthodes des triggers
        
        #fichiers tmx et décodage
        self.world_id = world
        self.world_tmx_path = os.path.join("..\\worlds",f"world{self.world_id}.tmx")
        self.world_tmx = pytmx.load_pygame(self.world_tmx_path,allow_duplicate_names=True)
        
        #textures
        self.enemy_imgs = load_enemy_imgs()
        self.spike_imgs = load_spike_imgs()
        self.switch_imgs = load_switches_imgs()
        self.door_imgs = load_door_imgs()
        
        #pygame sprite groups
        self.visible_blocks = Camera(world)
        self.collision_blocks = pygame.sprite.Group() 
        self.trigger_blocks = pygame.sprite.Group() 
        self.npcs = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.spikes = pygame.sprite.Group()
        self.switches = pygame.sprite.Group()
        self.doors = pygame.sprite.Group()
        self.terminals = pygame.sprite.Group()
        self.items = pygame.sprite.Group()

        self.player = None

        #npc path
        npc_path = {}
        npcs = []
        
        for layer in self.world_tmx.layers:
            if layer.name == "collision":
                for collider in layer:
                    Case(collider.x,collider.y, [self.collision_blocks], None, pygame.Surface((collider.width,collider.height)))
            if layer.name == "entitees":
                for entity in layer:

                    if entity.name == "player" and player_gen:
                        self.player = Player(entity.x,entity.y, self.visible_blocks, self.collision_blocks, player_life, player_max_life)
                    elif entity.name == 'npc':
                        npcs.append(Npc(entity.x,entity.y, entity.image,[self.visible_blocks, self.npcs],entity.npc_name,entity.talkable, entity.indicator, entity.first_dialog))
                        
                        # if tile_properties["class"] not in npc_path:
                        #     npc_path[tile_properties["class"].split(':')[1]] = {"npc_pos": (x, y), "npc_trajectoire": []}
                        # else:
                        #     npc_path[tile_properties["class"].split(':')[1]]["npc_pos"] = (x, y)
                        
                    elif entity.name == 'enemy':                         
                        Enemy(entity.x,entity.y,entity.image,[self.visible_blocks, self.enemies], self.collision_blocks, self.enemy_imgs, entity.movement,entity.enemy_name, self.items, entity.speed,entity.damages,entity.health)
                    
                    elif entity.name == "door":
                        Door(entity.x,entity.y,[self.collision_blocks,self.visible_blocks,self.doors],self.door_imgs,entity.properties["id"],entity.properties["locked"])
                    elif entity.name=="terminal":
                        Terminal(entity.x,entity.y,[self.visible_blocks,self.collision_blocks,self.terminals], entity.properties["id"],entity.properties["locked"])
                    elif entity.name=="spikes":
                        Spike(entity.x,entity.y,image, [self.visible_blocks, self.spikes], self.spike_imgs,"spike")

            if layer.name == "ground props":
                for x,y,gid in layer.iter_data():
                    if gid!=0:
                        tile_properties = self.world_tmx.get_tile_properties_by_gid(gid)
                        image = self.world_tmx.get_tile_image_by_gid(gid)
                        Case(x*CASE_SIZE, y*CASE_SIZE, [self.visible_blocks], image, basey=(y+int(str(tile_properties["class"])[1:]))*CASE_SIZE)

            if layer.name == "triggers":
                for trigger in layer:
                    trigger_args = trigger.properties["args"]
                    trigger_args = convert_to_tuple(trigger_args)
                    
                    Trigger(trigger.x,trigger.y, [self.trigger_blocks], None, trigger.properties["function"], trigger.width, trigger.height, *trigger_args)
            
            if layer.name == "switches":
                for switch in layer:
                    function_to_call = switch.properties["function_to_call"]
                    x = switch.x
                    y = switch.y
                    image = switch.image
                    if switch.name == "floor_lever":
                        Lever(x , y ,image, [self.collision_blocks,self.visible_blocks, self.switches], self.switch_imgs[f"floor_lever{switch.properties['type']}"], function_to_call, "lever")

                    elif switch.name == "pressure_plate":
                        PressurePlate(x , y ,image, [self.visible_blocks, self.switches], self.switch_imgs[f"pressure_plate{switch.properties['type']}"], function_to_call, "pressure_plate")
                        
                    elif switch.name == "manivelle":
                        Manivelle(x , y ,image, [self.collision_blocks,self.visible_blocks, self.switches], self.switch_imgs["manivelle"], function_to_call, "manivelle", switch.properties["has_manivelle"])
                        
                    elif switch.name == "wall_lever":
                        Lever(x , y ,image, [self.visible_blocks, self.switches], self.switch_imgs["wall_lever"], function_to_call, "lever",basey=y+switch.properties['height']*CASE_SIZE +1)
                            
            if layer.name == "npc_path":

                for x,y,gid in layer.iter_data():
                    if gid!=0:
                        tile_properties = self.world_tmx.get_tile_properties_by_gid(gid)
                        trigger_id = tile_properties["class"]
                        image = self.world_tmx.get_tile_image_by_gid(gid)

                        if tile_properties["class"] not in npc_path:
                            npc_path[tile_properties["class"]] = {"npc_pos": (0, 0), "npc_trajectoire": []}

                        npc_path[tile_properties["class"]]["npc_trajectoire"].append((x, y))
        
        # trie les chemins de NPC afin qu'il puisse suivre une seul trajectoire
        for key in npc_path.keys():
            npc_path[key]["npc_trajectoire"] = self.trouver_chemin(npc_path[key]["npc_trajectoire"], npc_path[key]["npc_pos"])

        # ajoute les trajectoires aux npc
        for npc in npcs:
            npc.path = npc_path[npc.name]

    def trouver_chemin(self, coordonnees, coordonnee_depart):
        """Algorithme de parcours en profondeur (DFS)
        A partie d'une liste de position, les tries pour que chaque position soit à côté de la position précédente dans le tableau
        """
        chemin = [coordonnee_depart]
        visites = set()
        visites.add(coordonnee_depart)

        def dfs(coordonnee_actuelle):
            voisins = [(coordonnee_actuelle[0]+1, coordonnee_actuelle[1]),  # droite
                    (coordonnee_actuelle[0], coordonnee_actuelle[1]+1),  # bas
                    (coordonnee_actuelle[0]-1, coordonnee_actuelle[1]),  # gauche
                    (coordonnee_actuelle[0], coordonnee_actuelle[1]-1)]  # haut

            for voisin in voisins:
                if voisin in visites or voisin not in coordonnees:
                    continue
                visites.add(voisin)
                chemin.append(voisin)
                if voisin == coordonnees[-1]:
                    return True
                if dfs(voisin):
                    return True
                chemin.pop()
            return False

        dfs(coordonnee_depart)
        return chemin
