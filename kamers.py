import pathlib
import pygame
from items import Items

class Kamers:
    def __init__(self, kamer):
        self.kamer = kamer
        if self.kamer == "bureau":
            self.bureau()
        if self.kamer == "gang":
            self.gang()
        if self.kamer == "living":
            self.living()

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
        self.pijl_down = Items(580, 200, 30, 30, afbeeldingen_folder / "pijl_down.PNG")
        
        self.bureau_sprites.add(self.potten, self.pc, self.boek, self.portret, self.hamer, self.vuilbak, self.kast, self.pijl_down)

    def gang(self):
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
        
        self.gang_sprites.add(self.bureau_deur, self.living_deur, self.kastje, self.spiegel, self.tablet)
    


    def living(self):
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
        
        
        self.living_sprites.add(self.boekenlade, self.boekenkast, self.open_haard, self.tv, self.kast)

    def grow(self,sprite):
        Items.scale(self,sprite)
        
    def shrink(self,sprite):
        Items.rescale(self, sprite)
        