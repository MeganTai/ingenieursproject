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
from bureau import Bureau
from gang import Gang
from living import Living

class World:
    def __init__(self):
        DIM = 800
        self.DISPLAYSURF = pygame.display.set_mode((DIM, DIM * 3 // 4))
        
        #self.background = pygame.transform.scale(self.background, (750, 650))
        self.bureau = Bureau()
        self.living = Living()
        self.gang = Gang()

        self.background = self.bureau.background

        self.big_text_sprites = pygame.sprite.Group()
        self.text = Tekst("",0,1)
        self.big_text1 = Tekst("Er zijn 2 soorten teksten, een die hier staat",1,1)
        self.big_text2 = Tekst("en een die de muis volgt. om beide te laten",1,2)
        self.big_text3 = Tekst("verdwijnen: druk spatie_bar",1,3)
        self.big_text_sprites.add(self.big_text1,self.big_text2,self.big_text3)

        self.inventory_sprites = pygame.sprite.Group()
        self.inventory_items = pygame.sprite.Group()
        self.popup_sprites = pygame.sprite.Group()
        self.inventory_space = Inventory(528,41,107,522,(153,0,0),0,True,False)
        self.inventory_slots = [Inventory(544, 57,75,75,(102,51,0),1,False,False), Inventory(544,140,75,75,(102,51,0),2,False,False), Inventory(544,223,75,75,(102,51,0),3,False,False), Inventory(544,306,75,75,(102,51,0),4,False,False), Inventory(544,389,75,75,(102,51,0),5,False,False), Inventory(544,472,75,75,(102,51,0),6,False,False)]
        self.hamer = Items(563,82,24,42, "afbeeldingen/hamer.PNG")
        self.zaklamp = Items(386,399,24,42, "afbeeldingen/hamer.PNG")
        self.bureausleutel = Items(581,247,24,42, "afbeeldingen/hamer.PNG")
        self.livingsleutel = Items(386,399,24,42, "afbeeldingen/hamer.PNG")
        self.key_card = Items(386,399,24,42, "afbeeldingen/hamer.PNG")
        self.vuilbak = Items(580, 510, 60, 60, "afbeeldingen/vuilbak.PNG")
        #vergroot niet
        self.inventory_sprites.add(self.inventory_space,self.inventory_slots)
        #vergroot wel
        self.inventory_items.add(self.vuilbak)

        self.special_sprites = pygame.sprite.Group()
        self.eindcode_1_gevonden, self.eindcode_2_gevonden, self.eindcode_3_gevonden, self.eindcode_4_gevonden = False, False, False, False
        
        
    def act(self):
        event = pygame.event.wait()

        self.DISPLAYSURF.blit(self.background, (0, 0))
        
        # achtergrond veranderen in aanwezige kamer
        if self.background == self.bureau.background:
            self.bureau.bureau_sprites.draw(self.DISPLAYSURF)
        elif self.background == self.living.background:
            self.living.living_sprites.draw(self.DISPLAYSURF)
        elif self.background == self.gang.background:
            self.gang.gang_sprites.draw(self.DISPLAYSURF)
        
        self.inventory_sprites.draw(self.DISPLAYSURF)
        self.inventory_items.draw(self.DISPLAYSURF)
        self.popup_sprites.draw(self.DISPLAYSURF)
        self.special_sprites.draw(self.DISPLAYSURF)

        if self.inventory_slots[0].wordt_gebruikt == True:
            self.bureau.hamer.rect.topleft = pygame.mouse.get_pos()
        if self.inventory_slots[1].wordt_gebruikt == True:
            self.bureau.sleutel.rect.topleft = pygame.mouse.get_pos()
               
        if self.text.mode == True:
            self.text.text_sprite.rect.topleft = pygame.mouse.get_pos()
            self.DISPLAYSURF.blit(self.text.text_sprite.text, self.text.text_sprite.rect)
            for self.big_texts in self.big_text_sprites.sprites():
                self.DISPLAYSURF.blit(self.big_texts.text_sprite.text, self.big_texts.text_sprite.rect)

        
    def mouse_action(self):
        
        
        # gaat na in welke kame rwe zitten, en vergroot dan de sprites van die kamer waneer hover     
        if self.background == self.bureau.background:
            Bureau.sprite_vergroting(self,self.bureau)
        elif self.background == self.living.background:
            Living.sprite_vergroting(self,self.living)
        elif self.background == self.gang.background:
            Gang.sprite_vergroting(self,self.gang)

        
        #voor special_sprites en inventory_items wordt er geen code in nieuwe file gestoken, deze blijven zo (deze moeten op elk moment kunnen runnen, dus gan we ze niet in aparte specifieke file steken)
        for sprite in self.special_sprites.sprites():
            if sprite.rect.collidepoint(pygame.mouse.get_pos()):
                Items.scale(self,sprite)
            else:
                Items.rescale(self,sprite)
        for sprite in self.inventory_items.sprites():
            if sprite.rect.collidepoint(pygame.mouse.get_pos()):
                Items.scale(self,sprite)
            else:
                Items.rescale(self,sprite)
                            
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
            


            #actieveer inventory slot waar op geklikt wordt en deactieveerd de rest
            if self.inventory_space.rect.collidepoint(pygame.mouse.get_pos()):
                for slot in self.inventory_slots:
                    if slot.rect.collidepoint(pygame.mouse.get_pos()):
                        if slot.in_use:
                            for slots in self.inventory_slots:
                                slots.wordt_gebruikt = False
                            slot.wordt_gebruikt = True

            #indien we op kamer bureau zitten, wordt de code in file bureau hier overlopen (verminderd code in world file)   (gang en living nog niet geimplementeerd dus hier niet uit commentaar halen!)
            if self.background == self.bureau.background:
                Bureau.click_actie(self, self.bureau)
            elif self.background == self.living.background:   
                Living.click_actie(self,self.living)
            elif self.background == self.gang.background:
                Gang.click_actie(self,self.gang)

            # Vuilbak rechts benedenhoek 
            if self.inventory_slots[5].rect.collidepoint(pygame.mouse.get_pos()):
                for slots in self.inventory_slots:
                    if slot.wordt_gebruikt:
                        slot.wordt_gebruikt = False
                        slot.rect.center = (slot.x,slot.y)
                for sprite in self.popup_sprites.sprites():
                    self.popup_sprites.remove(sprite) 
                for sprite in self.special_sprites.sprites():
                    self.special_sprites.remove(sprite)
                    self.bureau.special_monalisa = None
                    #self.special_sprites.kill() 
       
    def space_bar(self):
        self.text.mode = False
        self.text = Tekst("",0,1)
        for text in self.big_text_sprites.sprites():
            self.big_text_sprites.remove(text)