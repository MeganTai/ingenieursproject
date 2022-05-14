import pygame
from pygame.sprite import Group

class Items(pygame.sprite.Sprite):
    def __init__(self, x:int, y:int, width:int, height:int, afbeelding:str):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(afbeelding)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.afbeelding = afbeelding 
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.width = width
        self.height = height
        self.x = x
        self.y = y

    
    def scale(self,sprite):
        sprite.image = pygame.transform.scale(sprite.image, ((6/5)*sprite.width,(6/5)*sprite.height))
        
    
    def rescale(self,sprite):
        sprite.image = pygame.image.load(sprite.afbeelding)
        sprite.image = pygame.transform.scale(sprite.image, (sprite.width, sprite.height))