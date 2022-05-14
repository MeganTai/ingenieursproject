import pygame
from pygame.locals import *

from world import World
import time, sys
from eindgame import Eindgame

pygame.init()

FPS = pygame.time.Clock()

world = World()

pygame.display.set_caption("Escape-it")
World = pygame.display.set_mode((646, 605))
while True:
    events = pygame.event.get()
    FPS.tick(30)

    world.act()
    
    pygame.display.update()
    for event in events:
        print(event)
        if event.type == QUIT:
            pygame.quit() 
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            world.mouse_click()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                world.space_bar()
            if event.key == pygame.K_f:
                if world.background == world.eindgame.background:
                    Eindgame.deselect(world.eindgame)
        
        elif event.type == pygame.MOUSEMOTION:
            world.mouse_action()
        
            
        