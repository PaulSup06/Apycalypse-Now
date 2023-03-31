from settings import * 
from case import Case,Trigger
from debug import debug
from camera import Camera
from player import *
from npc import Npc, Door
from enemy import Enemy
from ui import Button
from browser import Terminal
import pytmx
import pygame
import os
import csv

class Level:
    def __init__(self, game, world=0,player_gen=True) -> None:
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
        self.door_imgs = load_door_imgs()
        
        #pygame sprite groups
        self.visible_blocks = Camera(world)
        self.collision_blocks = pygame.sprite.Group() 
        self.trigger_blocks = pygame.sprite.Group() 
        self.npcs = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
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
                            self.player = Player(x*CASE_SIZE,y*CASE_SIZE, self.visible_blocks, self.collision_blocks, default_player_life)
                        elif tile_properties["class"][:3] == 'npc':
                            #NPC de test (Fairy)
                            Npc(x*CASE_SIZE, y*CASE_SIZE,image,[self.visible_blocks, self.npcs],tile_properties["class"][4:],'True', first_dialog="1")
                        elif tile_properties["class"][:5] == 'enemy':
                            
                            Enemy(x*CASE_SIZE, y*CASE_SIZE,image,[self.visible_blocks, self.enemies],self.collision_blocks, self.enemy_imgs, "ligne_h",tile_properties["class"][6:])
                        
                        elif tile_properties["id"] == 29:
                            Door(x*CASE_SIZE,y*CASE_SIZE,[self.collision_blocks,self.visible_blocks,self.doors],self.door_imgs,False)
                        elif tile_properties["class"][:8]=="terminal":
                            Terminal(x*CASE_SIZE,y*CASE_SIZE,[self.visible_blocks,self.collision_blocks,self.terminals], 1,False)

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
