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

class Gang:
    def __init__(self):
        self.background = pygame.image.load("gang_afbeeldingen/gang_achtergrond.PNG")
        # 5 sprites : 2 deuren, 1 kast, 1 spiegel, 1 tablet  
        self.gang_sprites = pygame.sprite.Group()
        
        # de 5 sprites maken en dan in groep gang_sprites steken. 
        # (x-pos, y-pos, breedte, hoogte, afbeelding_naam)  

        afbeeldingen_folder = pathlib.Path("gang_afbeeldingen")

        self.bureau_deur = Items(24,161,48,48, afbeeldingen_folder / "deur.PNG")
        self.living_deur = Items(223,254,48,48, afbeeldingen_folder / "deur.PNG")
        self.kastje = Items(64,484,44,44, afbeeldingen_folder / "gereedschapkast.PNG")
        self.spiegel = Items(324,224,48,78, afbeeldingen_folder / "spiegel.PNG")
        self.tablet = Items(370,529,34,27, afbeeldingen_folder / "tablet.PNG")
        
        self.gang_sprites.add(self.bureau_deur, self.living_deur, self.kastje, self.spiegel, self.tablet)


    def sprite_vergroting(self,room_loc):
        for sprite in room_loc.gang_sprites.sprites():
            if sprite.rect.collidepoint(pygame.mouse.get_pos()):
                Items.scale(self, sprite)
            else:
                Items.rescale(self, sprite)

        
    def click_actie(self,room_loc):

        #deur naar gang
            if room_loc.bureau_deur.rect.collidepoint(pygame.mouse.get_pos()):
                    self.text = Tekst("   Naar de bureau", 0, 1)
                    
                    self.background = self.bureau.background

        #deur naar living
            if room_loc.living_deur.rect.collidepoint(pygame.mouse.get_pos()):
                    self.text = Tekst("   naar de living", 0, 1)
                    
                    self.background = self.living.background