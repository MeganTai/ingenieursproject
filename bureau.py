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

    def sprite_vergroting(self,room_loc):
        for sprite in room_loc.bureau.bureau_sprites.sprites():
            if sprite.rect.collidepoint(pygame.mouse.get_pos()):
                Kamers.grow(self,sprite)
            else:
                Kamers.shrink(self,sprite)


        
        
    def click_actie(self,room_loc):

        #volledige programma voor de 7 potten
            for pot in room_loc.bureau.potten:
                if pot.rect.collidepoint(pygame.mouse.get_pos()):
                        if self.inventory_slots[0].wordt_gebruikt:
                            if str(pot.afbeelding) == "afbeeldingen/gebroken_pot.PNG":
                                if pot == room_loc.bureau.potten[4]:
                                    self.text = Tekst("   Er zat een sleutel in!",0,1)
                                else:
                                    self.text = Tekst("   Er zat niks in.",0,1)

                            if str(pot.afbeelding) == "afbeeldingen/pot.PNG":
                                if pot == room_loc.bureau.potten[4]:
                                    pot.afbeelding = "afbeeldingen/gebroken_pot.PNG"
                                    pot.image = pygame.image.load(room_loc.bureau.pot_5.afbeelding)
                                    pot.image = pygame.transform.scale(room_loc.bureau.pot_5.image, (36,36))
                                    self.text = Tekst("   er zat een sleutel in de pot!",0,1)
                                    room_loc.bureau.sleutel = Items(581,177,50,50, "afbeeldingen/sleutel.PNG")
                                    room_loc.bureau.bureau_sprites.add(room_loc.bureau.sleutel)
                                    room_loc.inventory_slots[2].in_use = True
                                else:
                                    pot.afbeelding = "afbeeldingen/gebroken_pot.PNG"
                                    pot.image = pygame.image.load(room_loc.bureau.pot_1.afbeelding)
                                    pot.image = pygame.transform.scale(room_loc.bureau.pot_1.image, (36,36))
                                    self.text = Tekst("   er was niks in de pot",0,1)

                        else:
                            if str(pot.afbeelding) == "afbeeldingen\gebroken_pot.PNG":
                                if pot == room_loc.bureau.potten[4]:
                                    self.text = Tekst("   Er zat een sleutel in!",0,1)
                                else:
                                    self.text = Tekst("   Er zat niks in.",0,1)

                            if str(pot.afbeelding) == "afbeeldingen\pot.PNG":
                                if pot == room_loc.bureau.potten[4]:
                                    self.text = Tekst("   een pot... je ziet iets glimmend vanbinnen...",0,1)
                                else:
                                    self.text = Tekst("   een pot... zit er iets in?",0,1)
                
        # Schilderij Sterrennacht aan de muur
            if room_loc.bureau.portret.rect.collidepoint(pygame.mouse.get_pos()):                   
                self.big_text = Tekst("wat is het geboortejaar van deze schilder?",1,1)
                self.big_text_sprites.add(self.big_text)
                self.open_portret_sterrennacht = Items_popup(70,150,400, 300, pathlib.Path("afbeeldingen") / "sterrennacht.PNG")
                self.popup_sprites.add(self.open_portret_sterrennacht)
                room_loc.bureau.sterrennacht_gezien = True 
        
        # Open boek met stuk eindcode voor speler
            if room_loc.bureau.boek.rect.collidepoint(pygame.mouse.get_pos()):
                print("boek")
                self.big_text = Tekst("verzamel de overige stukken code doorheen dit spel...", 1, 1)
                self.big_text_sprites.add(self.big_text)
                self.open_boek = Items_popup(50,150,430,300, pathlib.Path("afbeeldingen") / "open_boek.PNG")
                self.popup_sprites.add(self.open_boek)
                
                if self.open_boek.rect.collidepoint(pygame.mouse.get_pos()):
        
                    self.big_text = Tekst("Hebbes! Nu nog op zoek naar de andere 3 stukken", 1, 1)
                    self.big_text_sprites.add(self.big_text)
                    self.special_eindcode_1 = Items_popup(275,250,155,47, pathlib.Path("afbeeldingen") / "eindcode_1.PNG")
                    self.special_sprites.add(self.special_eindcode_1)
                    self.eindcode_1_gevonden = True

        # Schilderij Mona Lisa in de kast
            if room_loc.bureau.special_monalisa is not None:
                if room_loc.bureau.special_monalisa.rect.collidepoint(pygame.mouse.get_pos()):
                    self.open_portret_monalisa = Items_popup(73,45,400, 510, pathlib.Path("afbeeldingen") / "mona_lisa.PNG")
                    self.popup_sprites.add(self.open_portret_monalisa)
                    room_loc.bureau.monalisa_gezien = True
                    # Special sprites verwijderen
                    for sprite in self.special_sprites.sprites():
                        self.special_sprites.remove(sprite)

        #pijl naar gang
            if room_loc.bureau.pijl_down.rect.collidepoint(pygame.mouse.get_pos()):
                    print("gang")
                    self.text = Tekst("   Terug naar de gang", 0, 1)
                    room_loc.bureau.bureau_pijl = True
                    self.background = self.gang.background   
        # pc vergrendeld en ontgrendeld
            if room_loc.bureau.pc.rect.collidepoint(pygame.mouse.get_pos()):                   
                    print("pc")
                    self.big_text = Tekst("voer de 2 geboortejaren in van de 2 schilders",1,1)
                    self.big_text_sprites.add(self.big_text)
                    self.open_pc = Items_popup(50,50,500, 500, pathlib.Path("afbeeldingen") / "computerscherm.PNG")
                    self.popup_sprites.add(self.open_pc)
                    if room_loc.bureau.monalisa_gezien == True and room_loc.bureau.sterrennacht_gezien == True:
                        # Spel openen
                        subprocess.run(["python", "fish_escape.py"]) 

        #kast programatie
            if room_loc.bureau.kast.rect.collidepoint(pygame.mouse.get_pos()):
                print("kast")
                if self.inventory_slots[2].in_use == True:
                    if self.inventory_slots[2].wordt_gebruikt == False:
                        self.text = Tekst("   misschien kunnen we de sleutel gebruiken?",0,1)
                    if self.inventory_slots[2].wordt_gebruikt == True:
                        self.text = Tekst("   de kast is nu open!",0,1)
                        self.open_kast = Items_popup(50,50,500, 500, pathlib.Path("afbeeldingen") / "groene_kast.PNG")
                        self.popup_sprites.add(self.open_kast)
                        room_loc.bureau.special_monalisa = Items(255,355,55,60, pathlib.Path("afbeeldingen") / "mona_lisa.PNG")
                        self.special_sprites.add(room_loc.bureau.special_monalisa)
                if self.inventory_slots[2].in_use == False:
                    self.text = Tekst("   de kast is op slot",0,1)

