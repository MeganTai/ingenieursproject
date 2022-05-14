from os import kill
import pygame
import random
from pygame.locals import *
import pathlib
import subprocess 

from items import Items
from items_popup import Items_popup
from inventory import Inventory
from tekst import Tekst


class Eindgame:
    def __init__(self):
        self.background = pygame.image.load("afbeeldingen/eindgame_achtergornd.png")
        self.background = pygame.transform.scale(self.background, (430,300))

        self.eindgame_sprites = pygame.sprite.Group()
        afbeeldingen_folder = pathlib.Path("afbeeldingen")
        self.special_eindcode = [Items(375,123,200,47, pathlib.Path("afbeeldingen") / "eindcode_1.PNG"), Items(375,336,300,82, pathlib.Path("afbeeldingen") / "eindcode_2.PNG"), Items(240,425,280,65, pathlib.Path("afbeeldingen") / "eindcode_3.PNG"), Items(350,247,590,75, pathlib.Path("afbeeldingen") / "eindcode_4.PNG")]
        self.eindgame_sprites.add(self.special_eindcode)
        self.geselecteerd = [False,False,False,False]

    def sprite_vergroting(self,room_loc):
        for sprite in room_loc.eindgame_sprites.sprites():
            if sprite.rect.collidepoint(pygame.mouse.get_pos()):
                Items.scale(self, sprite)
                print("scale")
            else:
                Items.rescale(self, sprite)
                print("rescale")

    def click_actie(self,room_loc):

        # wanneer er op een stuk code geklikt word, zal die geselecteerd worden als er geen andere geslecteerd is
        for i in range(len(room_loc.special_eindcode)):
            if room_loc.special_eindcode[i].rect.collidepoint(pygame.mouse.get_pos()):
                if room_loc.geselecteerd == [False, False, False, False]:
                    room_loc.geselecteerd[i] = True
                print(room_loc.geselecteerd)
       

    def deselect(self,room_loc):
        room_loc.geselecteerd = [False, False, False, False]
        print(room_loc.geselecteerd)
        if room_loc.special_eindcode[0].rect.y < room_loc.special_eindcode[1].rect.y - 50 < room_loc.special_eindcode[2].rect.y - 50 < room_loc.special_eindcode[3].rect.y - 50:
            self.inventory_items.add(self.key_card)
            self.inventory_slots[4].in_use = True
            self.background = self.bureau.background
            self.big_text = Tekst("De code is compleet! nu kunnen we hier weg!",1,1)
            self.big_text_sprites.add(self.big_text)

