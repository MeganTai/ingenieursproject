import pygame
from pygame.sprite import Group

class Items_popup(pygame.sprite.Sprite):
    def __init__(self, x:int, y:int, width:int, height:int, afbeelding:str):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(afbeelding)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.afbeelding = afbeelding        
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.width = width
        self.height = height

    def close(self):
        self.image = self.image
        self.afbeelding = self.afbeelding
    

