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

        self.boekenkast_gezien = False
        self.boekenlade_gezien = False
        self.special_geel_boek = None


    def sprite_vergroting(self,room_loc):
        for sprite in room_loc.living_sprites.sprites():
            if sprite.rect.collidepoint(pygame.mouse.get_pos()):
                Items.scale(self, sprite)
            else:
                Items.rescale(self, sprite)

      
    def click_actie(self,room_loc):

        #pijl naar gang
            if room_loc.pijl_down.rect.collidepoint(pygame.mouse.get_pos()):
                self.vuilbak_slot()
                self.space_bar()
                self.text = Tekst("   Terug naar de gang", 0, 1)
                    
                self.background = self.gang.background
        
        # zaklamp
            if room_loc.kast.rect.collidepoint(pygame.mouse.get_pos()):
                self.text = Tekst("   We hebben een zaklamp gevonden!",0,1)
                self.inventory_items.add(self.zaklamp)
                self.inventory_slots[1].in_use = True

        # livingsleutel
            if room_loc.open_haard.rect.collidepoint(pygame.mouse.get_pos()):
                if self.inventory_slots[1].wordt_gebruikt:
                    self.vuilbak_slot()
                    self.text = Tekst("   We hebben een sleutel gevonden!",0,1)
                    self.inventory_items.add(self.livingsleutel)
                    self.inventory_slots[3].in_use = True
            
        # boekenkast
            if room_loc.boekenkast.rect.collidepoint(pygame.mouse.get_pos()):
                if self.inventory_slots[3].in_use == True:
                    if self.inventory_slots[3].wordt_gebruikt == False:
                        self.text = Tekst("   Waarvoor dient deze sleutel?", 0, 1)
                    if self.inventory_slots[3].wordt_gebruikt == True:
                        self.vuilbak_slot()
                        self.text = Tekst("   De boekenkast is nu open!", 0, 1)
                        self.open_kast = Items(255, 300, 200, 400, pathlib.Path("living_afbeeldingen") / "boekenkast_3kleuren.PNG")
                        self.popup_sprites.add(self.open_kast)
                if self.inventory_slots[3].in_use == False:
                    self.text = Tekst("   De boekenkast is op slot", 0, 1)
        
        # boekenlade
            if room_loc.boekenlade.rect.collidepoint(pygame.mouse.get_pos()):
                self.big_text_sprites.add(Tekst("Waar heb ik deze boeken eerder al gezien...", 1, 1), Tekst("Zoek het verschil tussen de boeken.", 1, 2))
                room_loc.vier_boeken = Items(255, 300, 200, 200, pathlib.Path("living_afbeeldingen") / "4boeken.PNG")
                self.popup_sprites.add(room_loc.vier_boeken)
                room_loc.special_geelboek = Items(277, 310, 47, 170, pathlib.Path("living_afbeeldingen") / "geel_boek.PNG")
                self.special_sprites.add(room_loc.special_geelboek)
                if room_loc.special_geelboek.rect.collidepoint(pygame.mouse.get_pos()):
                    for sprite in self.popup_sprites.sprites():
                        self.popup_sprites.remove(sprite)
                    for sprite in self.special_sprites.sprites():
                        self.special_sprites.remove(sprite)

            if room_loc.special_geel_boek is not None:
                if room_loc.special_geel_boek.rect.collidepoint(pygame.mouse.get_pos()):
                    self.geelboek = Items(277, 310, 47, 170, pathlib.Path("living_afbeeldingen") / "geel_boek.PNG")
                    self.popup_sprites.add(self.geelboek)
                    room_loc.boekenlade_gezien = True

        # tv
            if room_loc.tv.rect.collidepoint(pygame.mouse.get_pos()):
                self.tv_groot = Items_popup(100, 180, 320, 270, pathlib.Path("living_afbeeldingen") / "tv_groot.PNG")
                self.popup_sprites.add(self.tv_groot)
                if room_loc.boekenkast_gezien == True and room_loc.boekenlade_gezien == True: 
                    subprocess.run(["python", "shoot_the_teacher.py"])
            