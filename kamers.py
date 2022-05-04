import pathlib
import pygame
from items import Items

class Kamers:
    def __init__(self, kamer):
        self.kamer = kamer
        
        if self.kamer == "gang":
            self.gang()
        if self.kamer == "living":
            self.living()

   
        

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
        