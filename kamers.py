import pathlib
import pygame
from items import Items

class Kamers:
    def __init__(self, kamer):
        self.kamer = kamer
        if self.kamer == "bureau":
            self.bureau()

    def bureau(self):
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
        self.hamer = Items(386,399,24,42, afbeeldingen_folder / "hamer.PNG")
        self.vuilbak = Items(580, 510, 60, 60, afbeeldingen_folder / "vuilbak.PNG")
        self.kast = Items(98,183,48,96, afbeeldingen_folder / "kast.PNG")
        
        self.bureau_sprites.add(self.potten, self.pc, self.boek, self.portret, self.hamer, self.vuilbak, self.kast)

    def grow(self,sprite):
        Items.scale(self,sprite)
        
    def shrink(self,sprite):
        Items.rescale(self, sprite)
        