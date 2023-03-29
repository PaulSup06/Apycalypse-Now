import pygame
from settings import *
from item import Item
import os
import random

class Inventaire:    
    def __init__(self, inventory=None) -> None:
        self.enabled = False
        self.cell_image = pygame.image.load("..\\textures\\ui\\cell.jpg")
        #Dictionary to hold images
        self.item_images = load_item_imgs()

        if not inventory:
            self.inventory = {}
        else:
            self.inventory = inventory
        
        self.inventory_grid,of = self.update_grid()

        #Init cursorPos
        self.cursor_y = 0
        self.cursor_x = 0
        
        self.item_name_display =''
        
    def update_grid(self):
        """Génère le tableau 3D contenant les items de l'inventaire

        Returns:
            inventory_grid: tableau 2D représentant l'inventaire
            overflow (list): liste des items dans le dict inventaire n'ayant pas pu être ajoutés à l'inventaire réel
        """
        inventory_grid = [[None] * GRID_SIZE for _ in range(GRID_SIZE)]
        overflow = []

        for key, value in self.inventory.items():
            elmt_pose = False
            x=0
            y=0
            overflow = []
            while not elmt_pose:
                if inventory_grid[y][x]==None:
                    if value > MAX_ITEMS_PER_CELL:
                        inventory_grid[y][x] = (key,MAX_ITEMS_PER_CELL)
                        value -= MAX_ITEMS_PER_CELL

                    else:
                        inventory_grid[y][x]=(key,value) 
                        elmt_pose = True
                        
                elif inventory_grid[y][x][0]==key:
                    amount_before = self.inventory_grid[y][x][0]
                    if value+amount_before > MAX_ITEMS_PER_CELL:
                        inventory_grid[y][x] = (key,MAX_ITEMS_PER_CELL)
                        value -= MAX_ITEMS_PER_CELL - amount_before

                    else:
                        self.inventory_grid[y][x] =(key, value + amount_before)
                        elmt_pose = True

                if not elmt_pose:                
                    x+=1
                    if x>=GRID_SIZE:
                        x=0
                        y+=1
                        if y>=GRID_SIZE:
                            overflow.append((key,value))
                            elmt_pose = True 
                    
              
        return inventory_grid, overflow


    def move_cursor(self,key,settings):
        if key == int(settings["k_up"]) and self.cursor_y>0:
            self.cursor_y -= 1
        elif key == int(settings["k_down"]) and self.cursor_y<GRID_SIZE-1:
            self.cursor_y +=1
        elif key == int(settings["k_left"]) and self.cursor_x>0:
            self.cursor_x -= 1
        elif key == int(settings["k_right"]) and self.cursor_x<GRID_SIZE-1:
            self.cursor_x +=1

        
    def draw_inventory(self, surface):
        self.rendered = pygame.Surface((WIDTH,HEIGHT), pygame.SRCALPHA)
        name_bg_rect = pygame.Rect(0,0,GRID_SIZE * (CASE_SIZE + CELL_MARGIN), 30)
        pygame.draw.rect(self.rendered, BACKGROUND_COLOR, name_bg_rect)

        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                cell_rect = pygame.Rect(
                    j * (CASE_SIZE + CELL_MARGIN),
                    i * (CASE_SIZE + CELL_MARGIN) + name_bg_rect.height +10,
                    CASE_SIZE,
                    CASE_SIZE
                )
                self.rendered.blit(self.cell_image, cell_rect)
                if self.inventory_grid[i][j] != None:
                    item_name, amount = self.inventory_grid[i][j]
                    item_image = self.item_images.get(item_name)

                    if item_image is not None:
                        item_image_rect = item_image.get_rect(center=cell_rect.center)
                        self.rendered.blit(item_image, item_image_rect)

                    if amount > 1:
                        font = pygame.font.SysFont(None, 24)
                        text = font.render(f"{amount}", True, (0, 0, 0))
                        text_rect = text.get_rect(bottomright=(cell_rect.right - 4, cell_rect.bottom - 4))
                        self.rendered.blit(text, text_rect)

                    if i == self.cursor_y and j == self.cursor_x:
                        if item_name != "":
                            font = pygame.font.SysFont(None, 24)
                            name_text = font.render(item_name, True, (255, 255, 255))
                            name_text_rect = name_text.get_rect(
                                midtop=((GRID_SIZE * (CASE_SIZE + CELL_MARGIN)) / 2,10))
                            self.rendered.blit(name_text, name_text_rect)
                            self.item_name_display = item_name
                        pygame.draw.rect(self.rendered, CURSOR_COLOR, cell_rect, 2)

                elif i == self.cursor_y and j == self.cursor_x:
                    pygame.draw.rect(self.rendered, CURSOR_COLOR, cell_rect, 2)
                    self.item_name_display = ""

        if self.item_name_display != "":
            font = pygame.font.SysFont(None, 24)
            name_text = font.render(self.item_name_display, True, (255, 255, 255))
            name_text_rect = name_text.get_rect(
                midtop=((GRID_SIZE * (CASE_SIZE + CELL_MARGIN)) / 2, 10))
            self.rendered.blit(name_text, name_text_rect)
        self.rendered_rect = self.rendered.get_bounding_rect()
        surface.blit(self.rendered, (
            (WIDTH-self.rendered_rect.width)//2,
            (HEIGHT-self.rendered_rect.height)//2
        ))

    def add_item(self, item_name, amount=1):
        """Ajoute un item à l'inventaire

        Args:
            item_name (str): nom de l'item à ajouter
            amount (int, optional): nombre d'items à ajouter. Defaults to 1.
        return:
            overflow (list): Liste d'items avec leur nombre qui n'ont pas pu être ajoutés à l'inventaire
        """
        if item_name in self.inventory.keys():
            amount_before = self.inventory[item_name]
            self.inventory[item_name] = amount + amount_before
        else:
            self.inventory[item_name]=amount

        self.inventory_grid, overflow = self.update_grid()
        for item,value in overflow:
            self.remove_item(item,value)
            
        return overflow

    def remove_item(self, item_name, amount=1):
        """Retire un item de l'inventaire

        Args:
            item_name (str): nom de l'item à retirer
            amount (int, optional): nombre d'items à retirer. Defaults to 1.

        Returns:
            Int: nombre d'items effectivement retirés (None si aucun disponible)
        """
        if item_name in self.inventory.keys():
            amount_before = self.inventory[item_name]
            if amount>amount_before:
                amount = amount_before
                
            self.inventory[item_name] = amount_before - amount
            if self.inventory[item_name] == 0:
                self.inventory.pop(item_name) 

            self.inventory_grid,of = self.update_grid()
            return amount
        
        return None       

    def drop(self, player, item_name, item_groups, amount=1):
        amount = self.remove_item(item_name, amount)
        if amount:
            offset = random.randint(0,100)
            positive = random.choice((-1,1))
            Item(player.x+(offset*positive),player.rect.bottom + 20,self.item_images[item_name],item_groups,item_name,amount)