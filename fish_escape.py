import time
import pygame
import random

from pygame.locals import *

white = (255, 255, 255)
lightskyblue = (176, 226, 255)
pygame.init()

surfaceWidth = 800
surfaceHeight = 500
surface = pygame.display.set_mode((surfaceWidth, surfaceHeight))
pygame.display.set_caption("Fish Escape")
clock = pygame.time.Clock()

img = pygame.image.load("afbeeldingen/vis.png")
img_width = img.get_size()[0]
img_height = img.get_size()[1]


def main():
    x = 150
    y = 200
    y_move = 0

    x_block = surfaceWidth
    y_block = 0

    block_width = 50
    block_height = random.randint(0, surfaceHeight / 2)
    gap = img_height * 3.1

    # snelheid van de blokken
    block_move = 5

    score = 0
    game_over = False
    background_image = pygame.image.load("afbeeldingen/onderwater.png")
    background_image = pygame.transform.scale(
        background_image, (surfaceWidth, surfaceHeight)
    )
    i = 0

    # Game Loop
    while not game_over:
        surface.fill((0, 0, 0))
        surface.blit(background_image, [i, 0])
        surface.blit(background_image, (surfaceWidth + i, 0))
        if i == -surfaceWidth:
            surface.blit(background_image, (surfaceWidth + i, 0))
            i = 0
        i -= 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    y_move = -3

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    y_move = 3

        y = y + y_move

        vis(x, y, img)
        show_score(score)
        updateFile(score)

        if 5 <= score < 15:
            gap = img_height * 2.9

        if 15 <= score < 25:
            block_move = 6.5
            gap = img_height * 2.7

        if score >= 25:
            block_move = 6.5
            gap = img_height * 2.5

        blocks(x_block, y_block, block_width, block_height, gap)
        x_block -= block_move

        # aanraking bij randen window
        if y > surfaceHeight - img_height or y < 0:
            msg_surface(score)

        # loop van de blokken
        if x_block < (-1 * block_width):
            x_block = surfaceWidth
            block_height = random.randint(0, surfaceHeight / 2)

        # puntentelling
        if x_block == x:
            score += 1

        # blokken aanraken
        if x + img_width > x_block and x < x_block + block_width:
            if y < block_height or y + img_height > block_height + gap:
                msg_surface(score)

        # if x > x_block + block_width and x < x_block + block_width + img_width / 5 and x_block == x:
        # µ    score += 1

        pygame.display.update()
        clock.tick(90)


def updateFile(current_score):
    f = open("scores.txt", "r")
    file = f.readlines()
    last = int(file[0])

    if last < int(current_score):
        f.close()
        file = open("scores.txt", "w")
        file.write(str(current_score))
        file.close()

        return current_score
    return last


def show_score(current_score):
    font = pygame.font.Font("freesansbold.ttf", 20)
    text = font.render("Score:" + str(current_score), True, lightskyblue)
    surface.blit(text, [3, 3])


def blocks(x_block, y_block, block_width, block_height, gap):
    pygame.draw.rect(
        surface, lightskyblue, [x_block, y_block, block_width, block_height]
    )
    pygame.draw.rect(
        surface,
        lightskyblue,
        [x_block, y_block + block_height + gap, block_width, surfaceHeight],
    )


def makeTextObjs(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()


def replay_or_quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        elif event.type == pygame.KEYUP:
            continue

        return pygame.K_SPACE


def msg_surface(current_score):
    smallText = pygame.font.Font("freesansbold.ttf", 20)
    largeText = pygame.font.Font("freesansbold.ttf", 130)
    mediumText = pygame.font.Font("freesansbold.ttf", 50)

    gameOverSurface, gameOverRect = makeTextObjs("Game Over", largeText)
    gameOverRect.center = surfaceWidth / 2, ((surfaceHeight / 2) - 125)
    surface.blit(gameOverSurface, gameOverRect)

    textSurface, textRect = makeTextObjs("Press any key to continue", smallText)
    textRect.center = surfaceWidth / 2, ((surfaceHeight) - 50)
    surface.blit(textSurface, textRect)

    lastScore, lastScoreRect = makeTextObjs(
        "Best Score: " + str(updateFile(current_score)), mediumText
    )
    lastScoreRect.center = surfaceWidth / 2, ((surfaceHeight / 2) + 70)
    surface.blit(lastScore, lastScoreRect)

    currentScore, currentScoreRect = makeTextObjs(
        "Score: " + str(current_score), mediumText
    )
    currentScoreRect.center = surfaceWidth / 2, (surfaceHeight / 2)
    surface.blit(currentScore, currentScoreRect)

    pygame.display.update()
    time.sleep(1)

    while replay_or_quit() is None:
        clock.tick()
    main()


# def gameOver():
#    msg_surface(score)


def vis(x, y, image):
    surface.blit(image, (x, y))


main()
pygame.quit()
quit()
