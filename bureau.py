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


class Bureau:
    def __init__(self):
        self.background = pygame.image.load("afbeeldingen/achtergrond_kamer_1.png")
        # 12 sprites : 7 potten, 1 kast, 1 pc, 1 boek, 1 portret en 1 hamer  
        self.bureau_sprites = pygame.sprite.Group()
        # de 12 sprites maken en dan in groep bureau_sprites steken. 
        # (x-pos, y-pos, breedte, hoogte, afbeelding_naam)  
        afbeeldingen_folder = pathlib.Path("afbeeldingen")
        self.potten = [Items(145,207,36,36, afbeeldingen_folder / "pot.PNG"), Items(145,303,36,36, afbeeldingen_folder / "pot.PNG"), Items(145,399,36,36, afbeeldingen_folder / "pot.PNG"), Items(145,495,36,36, afbeeldingen_folder / "pot.PNG"),Items(290,303,36,36, afbeeldingen_folder / "pot.PNG"), Items(290,399,36,36, afbeeldingen_folder / "pot.PNG"),Items(386,495,36,36, afbeeldingen_folder / "pot.PNG")]
        self.pc = Items(199,197,51,34, afbeeldingen_folder / "pc.png")
        self.boek = Items(241,200,18,21, afbeeldingen_folder / "eboek.PNG")
        self.portret = Items(409,112,94,47, afbeeldingen_folder / "portret.PNG")
        self.kast = Items(98,183,48,96, afbeeldingen_folder / "kast.PNG")
        self.pijl_down = Items(225, 500, 50, 50, afbeeldingen_folder / "pijl_down.PNG")
        self.bureau_sprites.add(self.potten, self.pc, self.boek, self.portret, self.kast, self.pijl_down)

        self.monalisa_gezien = False
        self.sterrennacht_gezien = False
        self.special_monalisa = None


    def sprite_vergroting(self,room_loc):
        for sprite in room_loc.bureau_sprites.sprites():
            if sprite.rect.collidepoint(pygame.mouse.get_pos()):
                Items.scale(self, sprite)
            else:
                Items.rescale(self, sprite)


    def click_actie(self,room_loc):

        #volledige programma voor de 7 potten
            for pot in room_loc.potten:
                if pot.rect.collidepoint(pygame.mouse.get_pos()):
                        if self.inventory_slots[0].wordt_gebruikt:
                            if str(pot.afbeelding) == "afbeeldingen\gebroken_pot.PNG":
                                if pot == room_loc.potten[4]:
                                    self.text = Tekst("   Er zat een sleutel in!",0,1)
                                else:
                                    self.text = Tekst("   Er zat niks in.",0,1)
                            if str(pot.afbeelding) == "afbeeldingen\pot.PNG":
                                if pot == room_loc.potten[4]:
                                    pot.afbeelding = "afbeeldingen\gebroken_pot.PNG"
                                    pot.image = pygame.image.load(pot.afbeelding)
                                    pot.image = pygame.transform.scale(pot.image, (36,36))
                                    self.text = Tekst("   er zat een sleutel in de pot!",0,1)
                                    self.inventory_items.add(self.bureausleutel)
                                    self.inventory_slots[2].in_use = True
                                else:
                                    pot.afbeelding = "afbeeldingen\gebroken_pot.PNG"
                                    pot.image = pygame.image.load(pot.afbeelding)
                                    pot.image = pygame.transform.scale(pot.image, (36,36))
                                    self.text = Tekst("   er was niks in de pot",0,1)
                        else:
                            if str(pot.afbeelding) == "afbeeldingen\gebroken_pot.PNG":
                                if pot == room_loc.potten[4]:
                                    self.text = Tekst("   Er zat een sleutel in!",0,1)
                                else:
                                    self.text = Tekst("   Er zat niks in.",0,1)
                            if str(pot.afbeelding) == "afbeeldingen\pot.PNG":
                                if pot == room_loc.potten[4]:
                                    self.text = Tekst("   een pot... je ziet iets glimmend vanbinnen...",0,1)
                                else:
                                    self.text = Tekst("   een pot... zit er iets in?",0,1)
                
        # Schilderij Sterrennacht aan de muur
            if room_loc.portret.rect.collidepoint(pygame.mouse.get_pos()):
                self.open_portret_sterrennacht = Items_popup(70,150,400, 300, pathlib.Path("afbeeldingen") / "sterrennacht.PNG")
                self.popup_sprites.add(self.open_portret_sterrennacht)
                room_loc.sterrennacht_gezien = True 
        
        # Open boek met stuk eindcode voor speler
            if room_loc.boek.rect.collidepoint(pygame.mouse.get_pos()):
                #opmaak boek
                self.space_bar()
                self.big_text_sprites.add(Tekst("verzamel de overige stukken code", 1, 1), Tekst("doorheen dit spel...", 1, 2))
                self.open_boek = Items_popup(50,150,430,300, pathlib.Path("afbeeldingen") / "open_boek.PNG")
                self.popup_sprites.add(self.open_boek)
                #kijkt voor de 4 stukken code 1 voor 1 na of deze gevonden is.
                if self.eindcode_2_gevonden == False:
                    with open("scores.txt", "r") as bestand:
                        score = bestand.read()
                        score = int(score.strip())
                        if score >= 20:
                            self.eindcode_2_gevonden = True
                if self.eindcode_3_gevonden == False:
                    with open("scores_stt.txt", "r") as bestand: 
                        score = bestand.read()
                        score = int(score.strip())
                        if score >= 30:
                            self.eindcode_3_gevonden = True
                if self.eindcode_4_gevonden == False:
                    with open("scores_worm.txt", "r") as bestand: 
                        score = bestand.read()
                        score = int(score.strip())
                        if score >= 20:
                            self.eindcode_4_gevonden = True
                if self.eindcode_1_gevonden == False:
                    self.space_bar()
                    self.big_text_sprites.add(Tekst("Hebbes! Nu nog op zoek naar de andere 3 delen", 1, 1))
                    self.eindcode_1_gevonden = True

                #toont de code indien deze gevonden is
                if self.eindcode_1_gevonden:
                    self.special_eindcode_1 = Items_popup(275,150,200,47, pathlib.Path("afbeeldingen") / "eindcode_1.PNG")
                    self.special_sprites.add(self.special_eindcode_1)
                if self.eindcode_2_gevonden:
                    self.special_eindcode_2 = Items_popup(225,295,300,82, pathlib.Path("afbeeldingen") / "eindcode_2.PNG")
                    self.special_sprites.add(self.special_eindcode_2)
                if self.eindcode_3_gevonden:
                    self.special_eindcode_3 = Items_popup(100,391,280,65, pathlib.Path("afbeeldingen") / "eindcode_3.PNG")
                    self.special_sprites.add(self.special_eindcode_3)
                if self.eindcode_4_gevonden:
                    self.special_eindcode_4 = Items_popup(55,210,600,75, pathlib.Path("afbeeldingen") / "eindcode_4.PNG")
                    self.special_sprites.add(self.special_eindcode_4)
                #start endgame wanneer alle stukken gevonden zijn
                if self.eindcode_1_gevonden and self.eindcode_2_gevonden and self.eindcode_3_gevonden and self.eindcode_4_gevonden:
                    self.vuilbak_slot()
                    self.background = self.eindgame.background

        # Schilderij Mona Lisa in de kast
            if room_loc.special_monalisa is not None:
                if room_loc.special_monalisa.rect.collidepoint(pygame.mouse.get_pos()):
                    self.open_portret_monalisa = Items_popup(73,45,400, 510, pathlib.Path("afbeeldingen") / "mona_lisa.PNG")
                    self.popup_sprites.add(self.open_portret_monalisa)
                    room_loc.monalisa_gezien = True
                    # Special sprites verwijderen
                    for sprite in self.special_sprites.sprites():
                        self.special_sprites.remove(sprite)

        #pijl naar gang
            if room_loc.pijl_down.rect.collidepoint(pygame.mouse.get_pos()):
                self.vuilbak_slot()
                self.space_bar()
                self.text = Tekst("   Terug naar de gang", 0, 1)
                self.background = self.gang.background

        # pc vergrendeld en ontgrendeld
            if room_loc.pc.rect.collidepoint(pygame.mouse.get_pos()):
                self.open_pc = Items_popup(50,50,500, 500, pathlib.Path("afbeeldingen") / "computerscherm.PNG")
                self.popup_sprites.add(self.open_pc)

                if room_loc.monalisa_gezien == True and room_loc.sterrennacht_gezien == True:
                    # Spel openen
                    subprocess.run(["python", "fish_escape.py"]) 

        #kast programatie
            if room_loc.kast.rect.collidepoint(pygame.mouse.get_pos()):
                if self.inventory_slots[2].in_use == True:
                    if self.inventory_slots[2].wordt_gebruikt == False:
                        self.text = Tekst("   misschien kunnen we de sleutel gebruiken?",0,1)
                    if self.inventory_slots[2].wordt_gebruikt == True:
                        self.vuilbak_slot()
                        self.space_bar()
                        self.text = Tekst("   de kast is nu open!",0,1)
                        self.open_kast = Items_popup(50,50,500, 500, pathlib.Path("afbeeldingen") / "groene_kast.PNG")
                        self.popup_sprites.add(self.open_kast)
                        room_loc.special_monalisa = Items(255,355,55,60, pathlib.Path("afbeeldingen") / "mona_lisa.PNG")
                        self.special_sprites.add(room_loc.special_monalisa)
                if self.inventory_slots[2].in_use == False:
                    self.text = Tekst("   de kast is op slot",0,1)

