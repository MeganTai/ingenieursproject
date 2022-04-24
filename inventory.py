import pygame
from items import Items
from pygame.sprite import Group

class Inventory(pygame.sprite.Sprite):
    def __init__(self,x,y,breedte,hoogte,kleur,slot,in_use,wordt_gebruikt):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((breedte, hoogte))
        self.image.fill(kleur)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.slot = slot
        self.in_use = in_use
        self.wordt_gebruikt = wordt_gebruikt
        hallo
      