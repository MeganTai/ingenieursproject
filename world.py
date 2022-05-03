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
from bureau import Bureau

class World:
    def __init__(self):
        DIM = 800
        self.DISPLAYSURF = pygame.display.set_mode((DIM, DIM * 3 // 4))
        
        #self.background = pygame.transform.scale(self.background, (750, 650))
        self.bureau = Bureau()
        self.living = Kamers("living")
        self.gang = Kamers("gang")

        self.background = self.bureau.bureau.background

        self.big_text_sprites = pygame.sprite.Group()
        self.text = Tekst("",0,1)
        self.big_text1 = Tekst("Er zijn 2 soorten teksten, een die hier staat",1,1)
        self.big_text2 = Tekst("en een die de muis volgt. om beide te laten",1,2)
        self.big_text3 = Tekst("verdwijnen: druk spatie_bar",1,3)
        self.big_text_sprites.add(self.big_text1,self.big_text2,self.big_text3)
        self.inventory_sprites = pygame.sprite.Group()
        self.popup_sprites = pygame.sprite.Group()
        self.inventory_space = Inventory(528,41,107,522,(153,0,0),0,True,False)
        self.inventory_slots = [Inventory(544, 57,75,75,(102,51,0),1,False,False), Inventory(544,140,75,75,(102,51,0),2,False,False), Inventory(544,223,75,75,(102,51,0),3,False,False), Inventory(544,306,75,75,(102,51,0),4,False,False), Inventory(544,389,75,75,(102,51,0),5,False,False), Inventory(544,472,75,75,(102,51,0),6,False,False)]
        self.inventory_sprites.add(self.inventory_space,self.inventory_slots)
        self.monalisa_gezien = False
        self.sterrennacht_gezien = False
        self.special_sprites = pygame.sprite.Group()
        self.eindcode_1_gevonden, self.eindcode_2_gevonden, self.eindcode_3_gevonden, self.eindcode_4_gevonden = False, False, False, False
        self.special_monalisa = None
        
    def act(self):
        event = pygame.event.wait()

        self.DISPLAYSURF.blit(self.background, (0, 0))
        self.inventory_sprites.draw(self.DISPLAYSURF)
        self.bureau.bureau.bureau_sprites.draw(self.DISPLAYSURF)
        #self.living.living_sprites.draw(self.DISPLAYSURF)
        #self.gang.gang_sprites.draw(self.DISPLAYSURF)
        self.popup_sprites.draw(self.DISPLAYSURF)
        self.special_sprites.draw(self.DISPLAYSURF)
        if self.inventory_slots[0].in_use == True:
            self.bureau.hamer.rect.topleft = pygame.mouse.get_pos()
        if self.inventory_slots[1].in_use == True:
            self.bureau.sleutel.rect.topleft = pygame.mouse.get_pos()
               
        if self.text.mode == True:
            Bureau.tekst_weergave(self, self.DISPLAYSURF)

        
    def mouse_action(self):
        
        Bureau.sprite_vergroting(self)

        for sprite in self.living.living_sprites.sprites():
            if sprite.rect.collidepoint(pygame.mouse.get_pos()):
                Kamers.grow(self,sprite)
            else:
                Kamers.shrink(self,sprite)

        for sprite in self.gang.gang_sprites.sprites():
            if sprite.rect.collidepoint(pygame.mouse.get_pos()):
                Kamers.grow(self,sprite)
            else:
                Kamers.shrink(self,sprite)

        for sprite in self.special_sprites.sprites():
            if sprite.rect.collidepoint(pygame.mouse.get_pos()):
                Kamers.grow(self,sprite)
            else:
                Kamers.shrink(self,sprite)
                            
    def mouse_click(self):
            
            # basisvorm om tekst op te laten komen: alles in if functie kopieren, 
            # en in tekst() geeft je gewenste tekst die op moet komen           
            # indien het kleine tekst is die de muis moet volgen:
            #   noem de text: self.text
            #   met 3 spaties vooraan om de tekst uit de weg van de muis te houden
            #   met als 2de en derde variabelen 0 en 1
            #
            #indien het grote tekst is die onderaan moet verschijnen:
            #   noem de text: self.big_text1 of 2 of 3 (niet self.text, die hoort bij kleine texten)
            #   geen spaties vooraan nodig
            #   2de variabele is 1
            #   3de variabele is een waarde die die lijn weergeeft.
            #       1 is 1ste lijn, 2 is 2de lijn, en 3 is 3de lijn  (momenteel enkel plaats voor 3)
            #       begin niet met 0!    
            #       gebruik meerdere lijnen indien de tekst te lang is om op 1 lijn te komen )
            #       (niet mogelijk om 1 grote tekst op meerdere lijnen te zetten, dus moeten we meerdere teksten onder elkaar zetten
            #   zet alles in de groep: self.big_text_sprites door: [self.big_text_sprites.(  hier de texten inzetten  )]
            
            if self.inventory_space.rect.collidepoint(pygame.mouse.get_pos()):
                for slot in self.inventory_slots:
                    if slots.rect.collidepoint(pygame.mouse.get_pos()):
                        if slot.in_use:
                            for slots in self.inventory_slots:
                                self.in_use = False
                            slot.in_use = True

            Bureau.click_actie(self)

            if self.bureau.vuilbak.rect.collidepoint(pygame.mouse.get_pos()):
    
                self.text = Tekst("   klik op de vuilbak om jouw huidige voorwerp los te laten",0,1)
     
            if self.inventory_slots[0].in_use == False:
                if self.bureau.hamer.rect.collidepoint(pygame.mouse.get_pos()):
        
                    self.text = Tekst("   een hamer, kan van pas komen.",0,1)
                    self.inventory_slots[0].in_use = True
                    self.bureau.hamer.rect.topleft = (563,82)
            if self.inventory_slots[0].in_use == True:
                if self.inventory_slots[0].in_use == False:
                    if self.inventory_slots[0].rect.collidepoint(pygame.mouse.get_pos()):
            
                        self.text = Tekst("   een hamer, kan van pas komen.",0,1)
                        self.inventory_slots[0].in_use = True
                if self.inventory_slots[0].in_use == True:
                    if self.inventory_slots[5].rect.collidepoint(pygame.mouse.get_pos()):
                        self.inventory_slots[0].in_use = False
                        self.bureau.hamer.rect.topleft = (563,82)
            
                        self.text = Tekst("",0,1)

            if self.inventory_slots[1].in_use == False:
                if self.bureau.kast.rect.collidepoint(pygame.mouse.get_pos()):
        
                    self.text = Tekst("   de kast is op slot",0,1)

            if self.inventory_slots[1].in_use == True:
                if self.inventory_slots[1].in_use == False:
                    if self.inventory_slots[1].rect.collidepoint(pygame.mouse.get_pos()):
            
                        self.text = Tekst("   waar dient deze sleutel voor?",0,1)
                        self.inventory_slots[1].in_use = True
                    if self.bureau.kast.rect.collidepoint(pygame.mouse.get_pos()):
            
                        self.text = Tekst("   misschien kunnen we de sleutel gebruiken?",0,1)
                if self.inventory_slots[1].in_use == True:
                    if self.inventory_slots[5].rect.collidepoint(pygame.mouse.get_pos()):
                        self.inventory_slots[1].in_use = False
                        self.bureau.sleutel.rect.center = (581,177)
            
                        self.text = Tekst("",0,1)
                    if self.bureau.kast.rect.collidepoint(pygame.mouse.get_pos()):
                        self.inventory_slots[1].in_use = False
                        self.bureau.sleutel.rect.center = (581,177)
            
                        self.text = Tekst("   de kast is nu open!",0,1)
                        self.open_kast = Items_popup(50,50,500, 500, pathlib.Path("afbeeldingen") / "groene_kast.PNG")
                        self.popup_sprites.add(self.open_kast)
                        self.special_monalisa = Items(255,355,55,60, pathlib.Path("afbeeldingen") / "mona_lisa.PNG")
                        self.special_sprites.add(self.special_monalisa)
                                        
                if self.bureau.pc.rect.collidepoint(pygame.mouse.get_pos()):                   

                    self.big_text = Tekst("voer de 2 geboortejaren in van de 2 schilders",1,1)
                    self.big_text_sprites.add(self.big_text)
                    self.open_pc = Items_popup(50,50,500, 500, pathlib.Path("afbeeldingen") / "computerscherm.PNG")
                    self.popup_sprites.add(self.open_pc)
                if self.monalisa_gezien == True and self.sterrennacht_gezien == True:
                    # Spel openen
                    subprocess.run(["python", "fish_escape.py"]) 
            
            # Schilderij Sterrennacht aan de muur
            if self.bureau.portret.rect.collidepoint(pygame.mouse.get_pos()):                   
    
                self.big_text = Tekst("wat is het geboortejaar van deze schilder?",1,1)
                self.big_text_sprites.add(self.big_text)
                self.open_portret_sterrennacht = Items_popup(70,150,400, 300, pathlib.Path("afbeeldingen") / "sterrennacht.PNG")
                self.popup_sprites.add(self.open_portret_sterrennacht)
                self.sterrennacht_gezien = True 

            # Schilderij Mona Lisa in de kast
            if self.special_monalisa is not None:
                if self.special_monalisa.rect.collidepoint(pygame.mouse.get_pos()):
                    self.open_portret_monalisa = Items_popup(73,45,400, 510, pathlib.Path("afbeeldingen") / "mona_lisa.PNG")
                    self.popup_sprites.add(self.open_portret_monalisa)
                    self.monalisa_gezien = True
                    # Special sprites verwijderen
                    for sprite in self.special_sprites.sprites():
                        self.special_sprites.remove(sprite) 

            # Open boek met stuk eindcode voor speler
            if self.bureau.boek.rect.collidepoint(pygame.mouse.get_pos()):
    
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
       
            # Vuilbak rechts benedenhoek 
            if self.inventory_slots[5].rect.collidepoint(pygame.mouse.get_pos()):
                for sprite in self.popup_sprites.sprites():
                    self.popup_sprites.remove(sprite) 
                for sprite in self.special_sprites.sprites():
                    self.special_sprites.remove(sprite)
                    self.special_monalisa = None
                    #self.special_sprites.kill() 
            
            if self.bureau.pijl_down.rect.collidepoint(pygame.mouse.get_pos()):
                self.text = Tekst("   Terug naar de gang", 0, 1)

    def space_bar(self):
        self.text.mode = False
        self.text = Tekst("",0,1)
        for text in self.big_text_sprites.sprites():
            self.big_text_sprites.remove(text)