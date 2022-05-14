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
from eindgame import Eindgame

class World:
    def __init__(self):
        DIM = 800
        self.DISPLAYSURF = pygame.display.set_mode((DIM, DIM * 3 // 4))
        
        #4 kamer aanmaken (hun achtergrond, sprites en variabelen aanmaken)
        self.bureau = Bureau()
        self.living = Living()
        self.gang = Gang()
        self.eindgame = Eindgame()

        self.background = self.bureau.background # eerste kamer wordt bureau.

        #de 3 files met highscore van de 3 minigames worden gereset.
        with open("scores.txt","w") as bestand:
            print("0", file=bestand)
        with open("scores_stt.txt","w") as bestand: 
            print("0", file=bestand)
        with open("scores_worm.txt","w") as bestand: 
            print("0", file=bestand)

        #alle spritegroepen uit world file worden aangemaakt.
        self.big_text_sprites = pygame.sprite.Group()
        self.inventory_sprites = pygame.sprite.Group()
        self.inventory_items = pygame.sprite.Group()
        self.popup_sprites = pygame.sprite.Group()
        self.special_sprites = pygame.sprite.Group()

        #introductie tekst.
        self.text = Tekst("",0,1)
        self.big_text1 = Tekst("Er zijn 2 soorten teksten, een die hier staat",1,1)
        self.big_text2 = Tekst("en een die de muis volgt. om beide te laten",1,2)
        self.big_text3 = Tekst("verdwijnen: druk spatie_bar",1,3)
        self.big_text_sprites.add(self.big_text1,self.big_text2,self.big_text3)

        #aanmaak van inventory en de inventory items.
        self.inventory_space = Inventory(528,41,107,522,(153,0,0),0,True,False)
        self.inventory_slots = [Inventory(544, 57,75,75,(102,51,0),1,False,False), Inventory(544,140,75,75,(102,51,0),2,False,False), Inventory(544,223,75,75,(102,51,0),3,False,False), Inventory(544,306,75,75,(102,51,0),4,False,False), Inventory(544,389,75,75,(102,51,0),5,False,False), Inventory(544,472,75,75,(102,51,0),6,False,False)]
        self.hamer = Items(588,100,24,42, "afbeeldingen/hamer.PNG")
        self.zaklamp = Items(580,180,55,50, "living_afbeeldingen/zaklamp.PNG")
        self.bureausleutel = Items(581,260,50,50, "afbeeldingen/sleutel.PNG")
        self.livingsleutel = Items(582,340,65,38, "living_afbeeldingen/livingsleutel.PNG")
        self.key_card = Items(580,420,24,42, "afbeeldingen/key_card.PNG")
        self.vuilbak = Items(580, 510, 60, 60, "afbeeldingen/vuilbak.PNG")

        #inventory en inventory items worden in aparte groepen gestoken zodat enkel inventory items sprite vergroting krijgen
        self.inventory_sprites.add(self.inventory_space,self.inventory_slots)
        self.inventory_items.add(self.vuilbak)

        #4 bool variabelen voor de eindcode stukken 
        self.eindcode_1_gevonden, self.eindcode_2_gevonden, self.eindcode_3_gevonden, self.eindcode_4_gevonden = False, False, False, False
        

    #functie om alles op het scherm te tekenen    
    def act(self):

        event = pygame.event.wait()
        self.DISPLAYSURF.blit(self.background, (0, 0))
        
        # achtergrond en sprites veranderen naar juiste kamer
        if self.background == self.bureau.background:
            self.bureau.bureau_sprites.draw(self.DISPLAYSURF)
        elif self.background == self.living.background:
            self.living.living_sprites.draw(self.DISPLAYSURF)
        elif self.background == self.gang.background:
            self.gang.gang_sprites.draw(self.DISPLAYSURF)
        elif self.background == self.eindgame.background:
            self.eindgame.eindgame_sprites.draw(self.DISPLAYSURF)
        
        #andere groepen sprites die altijd getoont moeten worden.
        self.inventory_sprites.draw(self.DISPLAYSURF)
        self.inventory_items.draw(self.DISPLAYSURF)
        self.popup_sprites.draw(self.DISPLAYSURF)
        self.special_sprites.draw(self.DISPLAYSURF)

        #item muis laten volgen: de inventory items of endgame code.
        if self.inventory_slots[0].wordt_gebruikt == True:
            self.hamer.rect.topleft = pygame.mouse.get_pos()
        if self.inventory_slots[1].wordt_gebruikt == True:
            self.zaklamp.rect.topleft = pygame.mouse.get_pos()
        if self.inventory_slots[2].wordt_gebruikt == True:
            self.bureausleutel.rect.topleft = pygame.mouse.get_pos()
        if self.inventory_slots[3].wordt_gebruikt == True:
            self.livingsleutel.rect.topleft = pygame.mouse.get_pos()
        if self.inventory_slots[4].wordt_gebruikt == True:
            self.key_card.rect.topleft = pygame.mouse.get_pos()
        for i in range(len(self.eindgame.geselecteerd)):
            if self.eindgame.geselecteerd[i]:
                self.eindgame.special_eindcode[i].rect.topleft = pygame.mouse.get_pos()

        #tekst op scherm zetten       
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
        elif self.background == self.eindgame.background:
            Eindgame.sprite_vergroting(self,self.eindgame)

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

            #activeer inventory slot waar op geklikt wordt en deactiveerd de rest
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
            elif self.background == self.eindgame.background:
                Eindgame.click_actie(self, self.eindgame)

            # Vuilbak rechts benedenhoek 
            if self.inventory_slots[5].rect.collidepoint(pygame.mouse.get_pos()):
                self.vuilbak_slot()

    #functie om tekst te verwijderen van het scherm
    def space_bar(self):
        self.text.mode = False
        self.text = Tekst("",0,1)
        for text in self.big_text_sprites.sprites():
            self.big_text_sprites.remove(text)

    #functie om inventory items, pop-ups en special sprites van het scherm te verwijderen
    def vuilbak_slot(self):
        for slot in self.inventory_slots:
            if slot.wordt_gebruikt:
                slot.wordt_gebruikt = False
                self.hamer.rect.center = (self.hamer.x, self.hamer.y)
                self.zaklamp.rect.center = (self.zaklamp.x, self.zaklamp.y)
                self.bureausleutel.rect.center = (self.bureausleutel.x, self.bureausleutel.y)
                self.livingsleutel.rect.center = (self.livingsleutel.x, self.livingsleutel.y)
                self.key_card.rect.center = (self.key_card.x, self.key_card.y)
            for sprite in self.popup_sprites.sprites():
                self.popup_sprites.remove(sprite) 
            for sprite in self.special_sprites.sprites():
                self.special_sprites.remove(sprite)
                self.bureau.special_monalisa = None