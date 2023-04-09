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
        self.world_tmx = pytmx.load_pygame(self.world_tmx_path)
        
        #textures
        self.enemy_imgs = load_enemy_imgs()
        self.spike_imgs = load_spike_imgs()
        (self.floor_lever1_imgs, self.floor_lever2_imgs, self.floor_lever3_imgs, self.manivelle_imgs, 
         self.pressure_plate1_imgs , self.pressure_plate2_imgs,  self.pressure_plate3_imgs, self.wall_lever_imgs) = load_switches_imgs()
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
        
        for layer in self.world_tmx.layers:
            if layer.name == "collision":
                for x,y,image in layer.tiles():
                    Case(x*CASE_SIZE, y*CASE_SIZE, [self.collision_blocks], image, pygame.Surface((CASE_SIZE, 32)))
            if layer.name == "entitees":
                for x,y,gid in layer.iter_data():
                    if gid!=0:
                        tile_properties = self.world_tmx.get_tile_properties_by_gid(gid)
                        if tile_properties["class"] == "player" and player_gen:
                            self.player = Player(x*CASE_SIZE,y*CASE_SIZE, self.visible_blocks, self.collision_blocks, player_life, player_max_life)
                        elif tile_properties["class"][:3] == 'npc':
                            #NPC de test (Fairy)
                            Npc(x*CASE_SIZE, y*CASE_SIZE,image,[self.visible_blocks, self.npcs],tile_properties["class"][4:],'True', first_dialog="1")
                        elif tile_properties["class"][:5] == 'enemy':                         
                            Enemy(x*CASE_SIZE, y*CASE_SIZE,image,[self.visible_blocks, self.enemies], self.collision_blocks, self.enemy_imgs, "ligne_h",tile_properties["class"][6:], self.items)
                       
                        elif tile_properties["class"][:4] == "door":
                            Door(x*CASE_SIZE,y*CASE_SIZE,[self.collision_blocks,self.visible_blocks,self.doors],self.door_imgs,tile_properties["class"][5:7],tile_properties["class"][8]=="1")
                        elif tile_properties["class"][:8]=="terminal":
                            Terminal(x*CASE_SIZE,y*CASE_SIZE,[self.visible_blocks,self.collision_blocks,self.terminals], tile_properties["class"][9:11],tile_properties["class"][12]=="1")
                        elif tile_properties["class"][:6]=="spikes":
                            Spike(x*CASE_SIZE, y*CASE_SIZE,image, [self.visible_blocks, self.spikes], self.collision_blocks, self.spike_imgs,"spike")

            if layer.name == "ground props":
                for x,y,gid in layer.iter_data():
                    if gid!=0:
                        tile_properties = self.world_tmx.get_tile_properties_by_gid(gid)
                        image = self.world_tmx.get_tile_image_by_gid(gid)
                        Case(x*CASE_SIZE, y*CASE_SIZE, [self.visible_blocks], image, basey=(y+int(str(tile_properties["class"])[1:]))*CASE_SIZE)

            if layer.name == "triggers":
                for x,y,gid in layer.iter_data():
                    if gid!=0:
                        tile_properties = self.world_tmx.get_tile_properties_by_gid(gid)
                        trigger_id = tile_properties["class"]
                        image = self.world_tmx.get_tile_image_by_gid(gid)
                        if trigger_id[:5]=="level":           
                            Trigger(x*CASE_SIZE, y*CASE_SIZE, [self.trigger_blocks], image,self.game.change_level,image,None,int(trigger_id[5:]))
                        if trigger_id[:8]=='poslevel':
                            
                            Trigger(x*CASE_SIZE, y*CASE_SIZE, [self.trigger_blocks], image,self.game.change_level,image,None,int(trigger_id[8:10]),trigger_id[10:])
                        elif trigger_id[:5]=="music":
                            Trigger(x*CASE_SIZE, y*CASE_SIZE, [self.trigger_blocks], image,self.game.play_music,image,None,f"{trigger_id[5:]}.wav")
            if layer.name == "switches":
                for x,y,gid in layer.iter_data():
                    if gid!=0:
                        tile_properties = self.world_tmx.get_tile_properties_by_gid(gid)
                        trigger_id = tile_properties["class"]
                        image = self.world_tmx.get_tile_image_by_gid(gid)

                        function_to_call =  getattr(layer, "class")

                        if "floor_lever1" in tile_properties["class"]:
                            Lever(x*CASE_SIZE, y*CASE_SIZE,image, [self.collision_blocks,self.visible_blocks, self.switches], self.collision_blocks, self.floor_lever1_imgs, function_to_call, "lever")
                        elif "floor_lever2" in tile_properties["class"]:
                            Lever(x*CASE_SIZE, y*CASE_SIZE,image, [self.collision_blocks,self.visible_blocks, self.switches], self.collision_blocks, self.floor_lever2_imgs, function_to_call, "lever")
                        elif "floor_lever3" in tile_properties["class"]:
                            Lever(x*CASE_SIZE, y*CASE_SIZE,image, [self.collision_blocks,self.visible_blocks, self.switches], self.collision_blocks, self.floor_lever3_imgs, function_to_call, "lever")
                        elif "pressure_plate1" in tile_properties["class"]:
                            PressurePlate(x*CASE_SIZE, y*CASE_SIZE,image, [self.visible_blocks, self.switches], self.collision_blocks, self.pressure_plate1_imgs, function_to_call, "pressure_plate")
                        elif "pressure_plate2" in tile_properties["class"]:
                            PressurePlate(x*CASE_SIZE, y*CASE_SIZE,image, [self.visible_blocks, self.switches], self.collision_blocks, self.pressure_plate2_imgs, function_to_call, "pressure_plate")
                        elif "pressure_plate3" in tile_properties["class"]:
                            PressurePlate(x*CASE_SIZE, y*CASE_SIZE,image, [self.visible_blocks, self.switches], self.collision_blocks, self.pressure_plate3_imgs, function_to_call, "pressure_plate")
                        elif "manivelle" in tile_properties["class"]:
                            Manivelle(x*CASE_SIZE, y*CASE_SIZE,image, [self.collision_blocks,self.visible_blocks, self.switches], self.collision_blocks, self.manivelle_imgs, function_to_call, "manivelle")
                        elif "wall_lever" in tile_properties["class"]:
                            Lever(x*CASE_SIZE, y*CASE_SIZE,image, [self.visible_blocks, self.switches], self.collision_blocks, self.wall_lever_imgs, function_to_call, "lever")

