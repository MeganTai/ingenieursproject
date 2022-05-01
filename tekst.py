import pygame
from pygame.sprite import Group

class Tekst(pygame.sprite.Sprite):
    def __init__(self, string, font_type,line):
        pygame.sprite.Sprite.__init__(self)
        zwart = (0,0,0)
        grijs = (224,224,224)
        if font_type == 0:
            self.font = pygame.font.Font('freesansbold.ttf', 12)
            self.text_sprite = pygame.sprite.Sprite()
            self.text_sprite.image = pygame.Surface((450, 150))
            self.text_sprite.image.fill(grijs)
            self.text_sprite.rect = self.text_sprite.image.get_rect()
            self.text_sprite.text = self.font.render(string,True, zwart, grijs)
            
        if font_type == 1:
            self.font = pygame.font.Font('freesansbold.ttf', 24)
            self.text_sprite = pygame.sprite.Sprite()
            self.text_sprite.image = pygame.Surface((450, 150))
            self.text_sprite.image.fill(grijs)
            self.text_sprite.rect = self.text_sprite.image.get_rect()
            self.text_sprite.text = self.font.render(string,True, zwart, grijs)
            self.text_sprite.rect.topleft = (50,500 + line*25)
        
        #hier op True zetten, in plaats in world, zorgt voor 1 lijn minder bij iedere text die we maken
        self.mode = True