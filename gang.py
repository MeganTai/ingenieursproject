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
        self.pijl_down = Items(225, 500, 50, 50, afbeeldingen_folder / "pijl_down.PNG")

        self.gang_sprites.add(self.bureau_deur, self.living_deur, self.kastje, self.spiegel, self.tablet, self.pijl_down)
        self.tablet_code = False

    def sprite_vergroting(self,room_loc):
        for sprite in room_loc.gang_sprites.sprites():
            if sprite.rect.collidepoint(pygame.mouse.get_pos()):
                Items.scale(self, sprite)
            else:
                Items.rescale(self, sprite)

        
    def click_actie(self,room_loc):

        #deur naar gang
            if room_loc.bureau_deur.rect.collidepoint(pygame.mouse.get_pos()):
                self.vuilbak_slot()
                self.space_bar()
                self.text = Tekst("   Naar bureau", 0, 1)
                    
                self.background = self.bureau.background

        #deur naar living
            if room_loc.living_deur.rect.collidepoint(pygame.mouse.get_pos()):
                self.vuilbak_slot()
                self.space_bar()
                self.text = Tekst("   naar de living", 0, 1)
                    
                self.background = self.living.background

        #hammer vinden
            if room_loc.kastje.rect.collidepoint(pygame.mouse.get_pos()):
                self.text = Tekst("   We hebben een hammer gevonden!",0,1)
                self.inventory_items.add(self.hamer)
                self.inventory_slots[0].in_use = True
        
        #spiegel
            if room_loc.spiegel.rect.collidepoint(pygame.mouse.get_pos()):
                if room_loc.spiegel.afbeelding == "":
                    self.text = Tekst("   er zat een code achter de spiegel",0,1)
                elif self.inventory_slots[0].wordt_gebruikt:
                    self.vuilbak_slot()
                    self.big_text_sprites.add(Tekst("   Er was een code achter de spiegel verstopt!",1,1), Tekst("   We kunnen nu de tablet openen!",1,2))
                    room_loc.spiegel.afbeelding = ""
                    room_loc.gang_sprites.remove(room_loc.spiegel)
                    room_loc.tablet_code = True
                else:
                    self.text = Tekst("   een spiegel, er lijkt iets achter te zitten...",0,1)
        #tablet
            if room_loc.tablet.rect.collidepoint(pygame.mouse.get_pos()):
                if room_loc.tablet_code == True:
                    print("start gang game")
                    #hier moet code om gang minigame te starten
        #ending    
            if room_loc.pijl_down.rect.collidepoint(pygame.mouse.get_pos()):
                if self.inventory_slots[4].wordt_gebruikt:
                    self.vuilbak_slot()
                    self.space_bar()
                    self.ending = Items_popup(0, 0, 646, 606, "afbeeldingen/ending.png")
                    self.popup_sprites.add(self.ending)
                else:

                    self.text = Tekst("   We kunnen nog niet weg! we hebben een key card nodig!", 0, 1)
                    
                    