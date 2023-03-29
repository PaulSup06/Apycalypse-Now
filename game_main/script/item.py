import pygame
from settings import *
from entity import Entity

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
        self.kill()
        return self.amount
    
    def handle(self,player,offset):
        self.draw(offset)
        if self.rect.colliderect(player.rect):
            return self.pickup()
        else:
            return None
        
    def stack(self,items):
        for item in items:
            if item!=self and item.name==self.name and self.check_distance_to((item.x,item.y), stackable_range) and item.amount<MAX_ITEMS_PER_CELL:
                total = self.amount + item.amount
                if total > MAX_ITEMS_PER_CELL:
                    item.amount = MAX_ITEMS_PER_CELL
                    self.amount = total - MAX_ITEMS_PER_CELL
                else:
                    item.amount += self.amount
                    return True
        
        
    def draw(self,offset):
        self.amount_rendered = font2.render(str(self.amount),1,"black")
        self.surface.blit(pygame.transform.scale(self.image, ITEM_SIZE),(self.x-offset.x,self.y-offset.y))
        self.surface.blit(self.amount_rendered,(self.x -offset.x + ITEM_SIZE[0] + 5,self.y - offset.y + ITEM_SIZE[1] + 5))
        