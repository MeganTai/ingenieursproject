from os import kill
import pygame
import random
from pygame.locals import *
import pathlib
import subprocess 

from items import Items
from inventory import Inventory
from tekst import Tekst
from items_popup import Items_popup

class Living:
    def __init__(self):
        self.background = pygame.image.load("living_afbeeldingen/living_achtergrond.PNG")
        # 5 sprites : 1 boekelade, 1 boekenkast, 1 kast, 1 tv, 1 open haard  
        self.living_sprites = pygame.sprite.Group()
        
        # de 5 sprites maken en dan in groep living_sprites steken. 
        # (x-pos, y-pos, breedte, hoogte, afbeelding_naam)  

        afbeeldingen_folder = pathlib.Path("living_afbeeldingen")
        
        self.boekenlade = Items(149,197,38,22, afbeeldingen_folder / "boekelade.png")
        self.boekenkast = Items(64,185,45,93, afbeeldingen_folder / "boekenkast.PNG")
        self.kast = Items(321,189,43,86, afbeeldingen_folder / "kast.PNG")
        self.open_haard = Items(407,159,130,115, afbeeldingen_folder / "open_haard.PNG")
        self.tv = Items(199, 200, 55, 39, afbeeldingen_folder / "tv.PNG")
        self.pijl_down = Items(125, 550, 50, 50, afbeeldingen_folder / "pijl_down.PNG")

        self.living_sprites.add(self.boekenlade, self.boekenkast, self.open_haard, self.tv, self.kast,self.pijl_down)


    def sprite_vergroting(self,room_loc):
        for sprite in room_loc.living_sprites.sprites():
            if sprite.rect.collidepoint(pygame.mouse.get_pos()):
                Items.scale(self, sprite)
            else:
                Items.rescale(self, sprite)

      
    def click_actie(self,room_loc):

        #pijl naar gang
            if room_loc.pijl_down.rect.collidepoint(pygame.mouse.get_pos()):
                    self.text = Tekst("   Terug naar de gang", 0, 1)
                    
                    self.background = self.gang.background