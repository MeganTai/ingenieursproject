import pygame
from pygame.locals import *

from world import World
import time, sys

pygame.init()

FPS = pygame.time.Clock()

world = World()

pygame.display.set_caption("escape_room versie 1")
World = pygame.display.set_mode((646, 605))
while True:
    events = pygame.event.get()
    FPS.tick(30)

    world.act()

    pygame.display.update()
    for event in events:
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            world.mouse_action()
        if event.type == pygame.MOUSEBUTTONDOWN:
            world.mouse_click()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                world.space_bar()
            
        