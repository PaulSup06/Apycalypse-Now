import pygame
from settings import *
from entity import Entity
import os
import random

class Inventaire:    
    def __init__(self, main, inventory=None) -> None:
        """Inventaire du joueur

        Args:
            main (Game): élément Game, utilisé pour faire référence à des fonctions de l'objet Game
            inventory (dict, optional): inventaire enregistré si besoin, sinon inventaire vide.
        """
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
        
        self.main_elmt = main
        self.item_function = {
            "life_potion":self.main_elmt.heal_player,
            "speed_potion":self.main_elmt.speed_player,
            "strength_potion":self.main_elmt.strength_player,
            "invincibility_potion":self.main_elmt.invincibility_player,
            "note":self.main_elmt.read_note,
            "heart":self.main_elmt.add_player_heart,
        }
        
    def have_item(self,name):
        return name in self.inventory

    def update_grid(self):
        """Génère le tableau 3D contenant les items de l'inventaire

        Returns:
            inventory_grid: tableau 2D représentant l'inventaire
            overflow (list): liste des items dans le dict inventaire n'ayant pas pu être ajoutés à l'inventaire réel
        """
        inventory_grid = [[None] * GRID_SIZE for _ in range(GRID_SIZE)]
        overflow = []

        for key, value in self.inventory.items():
            value = int(value)
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
        """Déplace le curseur du joueur dans l'inventaire

        Args:
            key (int): touche pygame pressée
            settings (dict): dictionnaire des paramètres de l'utilisateur et des touches attribuées
        """
        if key == int(settings["k_up"]) and self.cursor_y>0:
            self.cursor_y -= 1
        elif key == int(settings["k_down"]) and self.cursor_y<GRID_SIZE-1:
            self.cursor_y +=1
        elif key == int(settings["k_left"]) and self.cursor_x>0:
            self.cursor_x -= 1
        elif key == int(settings["k_right"]) and self.cursor_x<GRID_SIZE-1:
            self.cursor_x +=1

        
    def draw_inventory(self, surface, params):
        """Affichage de l'inventaire

        Args:
            surface (pygame.surface): Surface d'affichage de l'inventaire (généralement pygame.display)
            params (dict): dictionnaire des paramètres et des touches
        """
        self.rendered = pygame.Surface((WIDTH,HEIGHT), pygame.SRCALPHA)
        name_bg_rect = pygame.Rect(0,0,GRID_SIZE * (CASE_SIZE + CELL_MARGIN), 80)
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
                    item_image = self.item_images.get(item_name if "note" not in item_name else "note")

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

                            if item_names_render.get(item_name):
                                name_text = font.render(item_names_render[item_name], True, (255, 255, 255))
                            else:
                                name_text =  font.render(item_name, True, (255, 255, 255))

                            name_text_rect = name_text.get_rect(
                                midtop=((GRID_SIZE * (CASE_SIZE + CELL_MARGIN)) / 2,10))
                            
                            drop_text = font.render(f"[{pygame.key.name(int(params['k_attack']))}] pour lacher",1,"white")
                            self.rendered.blit(drop_text, (name_text_rect.centerx - drop_text.get_width()//2, name_text_rect.bottom + 5))
                            
                            if item_name in self.item_function.keys() or "note" in str(item_name):
                                verbe = "utiliser" if "note" not in str(item_name) else "lire"
                                action_text = font.render(f"[{pygame.key.name(int(params['k_interact']))}] pour " + verbe ,1,"white")
                                self.rendered.blit(action_text, (name_text_rect.centerx - action_text.get_width()//2, name_text_rect.bottom + drop_text.get_height() + 5))
                                
                            self.rendered.blit(name_text, name_text_rect)
                            self.item_name_display = item_name
                            
                        pygame.draw.rect(self.rendered, CURSOR_COLOR, cell_rect, 2)

                elif i == self.cursor_y and j == self.cursor_x:
                    pygame.draw.rect(self.rendered, CURSOR_COLOR, cell_rect, 2)
                    self.item_name_display = ""


        self.rendered_rect = self.rendered.get_bounding_rect()
        surface.blit(self.rendered, (
            (WIDTH-self.rendered_rect.width)//2,
            (HEIGHT-self.rendered_rect.height)//2
        ))

    def add_item(self, item_name, amount=1, args=""):
        """Ajoute un item à l'inventaire

        Args:
            item_name (str): nom de l'item à ajouter
            amount (int, optional): nombre d'items à ajouter. Defaults to 1.
        return:
            overflow (list): Liste d'items avec leur nombre qui n'ont pas pu être ajoutés à l'inventaire
        """
        amount = int(amount)
        if args != "":
            item_name = item_name + "|" + args

        if item_name in self.inventory.keys():
            amount_before = self.inventory[item_name]
            self.inventory[item_name] = amount + amount_before
        else:
            self.inventory[item_name]=amount

        self.inventory_grid, overflow = self.update_grid()
        for item,value in overflow:
            self.remove_item(item,value)

        # affiche petite bulle informant qu'on a reçu un item
        if item_names_render.get(item_name):
            item_name_rendered = item_names_render.get(item_name)
        else:
            item_name_rendered = item_name
        self.main_elmt.item_picked_up_animation = [True, item_name_rendered, amount, 0]
            
        return overflow

    def remove_item(self, item_name, amount=1):
        """Retire un item de l'inventaire

        Args:
            item_name (str): nom de l'item à retirer
            amount (int, optional): nombre d'items à retirer. Defaults to 1.

        Returns:
            Int: nombre d'items effectivement retirés (None si aucun disponible)
        """
        amount = int(amount)
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

    def drop(self, player, item_groups,item_name=None, amount=MAX_ITEMS_PER_CELL):
        """Lache un ou plusieurs items sur le sol

        Args:
            player (Player): objet du joueur
            item_groups (pygame.sprite.Group): group item du level
            item_name (str, optional): Nom de l'item à lacher. Par défaut, l'item sélectionné par le curseur du joueur.
            amount (int, optional): Nombre d'items à lacher. Par défaut un stack soit 64 items.
        """
        if not item_name:
            item = self.inventory_grid[self.cursor_y][self.cursor_x]
            if item:
                item_name=item[0]
            else:
                return False #cas ou le joueur drop une case vide
        
        amount = self.remove_item(item_name, amount)
        if amount:
            offset = random.randint(0,100)
            positive = random.choice((-1,1))
            Item(player.x+(offset*positive),player.rect.bottom + 20,self.item_images[item_name if "note" not in item_name else "note"],item_groups,item_name,amount)
    
    def use(self):
        """utilise l'objet sélectionné dans l'inventaire (consommable uniquement)
        """
        selected_item = self.inventory_grid[self.cursor_y][self.cursor_x]
        if selected_item != None:
            selected_item = selected_item[0]
            if  selected_item in self.item_function or 'note' in selected_item:
                if "note" in selected_item:
                    used = self.item_function["note"](selected_item)
                else:
                    used = self.item_function[selected_item]()
                    
                if used:
                    self.remove_item(selected_item,1)        
                
class Item(Entity):
    def __init__(self, x, y, image, groupes, name, amount):
        """Objet item lorsque laché au sol

        Args:
            x (int): position x de l'item
            y (int): position y de l'item
            image (pygame.image): image par défaut (non resized)
            groupes (list): list de pygame.sprite.Group auxquels ajouter l'item'
            name (str): Nom de l'item
            amount (int): quantité d'items dans le stack (max = MAX_ITEMS_PER_CELL)
        """
        super().__init__(x, y, image, groupes)
        self.name = name
        self.amount = amount
        self.rect = self.image.get_rect(topleft=(x,y))
        self.amount_rendered = font2.render(str(self.amount),1,"black")
        self.surface = pygame.display.get_surface()
    
    def pickup(self):
        """Ramasse un item au sol et supprime l'objet

        Returns:
            int: quantité ramassée
        """
        self.kill()
        return self.amount
    
    def handle(self,player,offset):
        """Gère l'objet, son affichage et sa distance par rapport au joueur

        Args:
            player (Player): objet du joueur
            offset (Camera.offset): offset pour l'affichage

        Returns:
            int: quantité ramassée par le joueur
        """
        self.draw(offset)
        if self.rect.colliderect(player.rect):
            return self.pickup()
        else:
            return None
        
    def stack(self,items):
        """Empile les items dans un même objet si plusieurs items du même type sont proches

        Args:
            items (group): level.item, groupe des items au sol

        Returns:
            bool: True si l'item a été empilé
        """
        for item in items:
            if item!=self and item.name==self.name and self.check_distance_to(item.rect.center, stackable_range) and item.amount<MAX_ITEMS_PER_CELL:
                total = self.amount + item.amount
                if total > MAX_ITEMS_PER_CELL:
                    item.amount = MAX_ITEMS_PER_CELL
                    self.amount = total - MAX_ITEMS_PER_CELL
                else:
                    item.amount += self.amount
                    return True
        
        
    def draw(self,offset):
        """Gère l'affichage de l'item sur l'écran

        Args:
            offset (Camera.offset): offset d'affichage
        """
        self.amount_rendered = font2.render(str(self.amount),1,"black")
        self.surface.blit(pygame.transform.scale(self.image, ITEM_SIZE),(self.x-offset.x,self.y-offset.y))
        self.surface.blit(self.amount_rendered,(self.x -offset.x + ITEM_SIZE[0] + 5,self.y - offset.y + ITEM_SIZE[1] + 5))
        