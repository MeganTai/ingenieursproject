from os import kill
import pygame
import random
from pygame.locals import *
import pathlib
import subprocess 

from kamers import Kamers
from items import Items
from inventory import Inventory
from tekst import Tekst
from items_popup import Items_popup


class Bureau:
    def __init__(self):
        self.bureau = Kamers("bureau")

    def sprite_vergroting(self):
        for sprite in self.bureau.
            if sprite.rect.collidepoint(pygame.mouse.get_pos()):
                Kamers.grow(self,sprite)
            else:
                Kamers.shrink(self,sprite)
    def tekst_weergave(self,surface):
        self.text.text_sprite.rect.topleft = pygame.mouse.get_pos()
        surface.blit(self.text.text_sprite.text, self.text.text_sprite.rect)
        for self.big_texts in self.big_text_sprites.sprites():
            surface.blit(self.big_texts.text_sprite.text, self.big_texts.text_sprite.rect)
        
    def click_actie(self):
        for pot in self.bureau.potten:
                if pot.rect.collidepoint(pygame.mouse.get_pos()):
                    if self.inventory_slots[0].in_use:

                        if pot.afbeelding == "afbeeldingen/gebroken_pot.PNG":
                            if pot == self.bureau.potten[4]:
                                self.text = Tekst("   Er zat een sleutel in!",0,1)
                            else:
                                self.text = Tekst("   Er zat niks in.",0,1)

                        if pot.afbeelding == "afbeeldingen/pot.PNG":
                            if pot == self.bureau.potten[4]:
                                pot.afbeelding = "afbeeldingen/gebroken_pot.PNG"
                                pot.image = pygame.image.load(self.bureau.pot_5.afbeelding)
                                pot.image = pygame.transform.scale(self.bureau.pot_5.image, (36,36))
                                self.text = Tekst("   er zat een sleutel in de pot!",0,1)
                                self.bureau.sleutel = Items(581,177,50,50, "afbeeldingen/sleutel.PNG")
                                self.bureau.bureau_sprites.add(self.bureau.sleutel)
                                self.inventory_slots[2].in_use = True
                            else:
                                pot.afbeelding = "afbeeldingen/gebroken_pot.PNG"
                                pot.image = pygame.image.load(self.bureau.pot_1.afbeelding)
                                pot.image = pygame.transform.scale(self.bureau.pot_1.image, (36,36))
                                self.text = Tekst("   er was niks in de pot",0,1)

                    else:
                        if pot.afbeelding == "afbeeldingen/gebroken_pot.PNG":
                            if pot == self.bureau.potten[4]:
                                self.text = Tekst("   Er zat een sleutel in!",0,1)
                            else:
                                self.text = Tekst("   Er zat niks in.",0,1)
                            
                        if pot.afbeelding == "afbeeldingen/pot.PNG":
                            if pot == self.bureau.potten[4]:
                                self.text = Tekst("   een pot... je ziet iets glimmend vanbinnen...",0,1)
                            else:
                                self.text = Tekst("   een pot... zit er iets in?",0,1)
                        