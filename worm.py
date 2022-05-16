import pygame
import time
import random
import sys

width = 800
height = 509

white = (255, 255, 255)
worm_color = (255, 185, 185)
red = (255, 0, 0)
durt = (230, 120, 0)

pygame.init()

pygame.display.set_caption("Worm")
icon = pygame.image.load("afbeeldingen/worm.png")
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((width, height))


background = pygame.image.load("afbeeldingen/aarde.png")
background = pygame.transform.scale(background, (width, height))

clock = pygame.time.Clock()


def show_score(current_score):
    font = pygame.font.Font("freesansbold.ttf", 20)
    score = font.render("Score: " + str(current_score), True, white)
    screen.blit(score, (10, 10))


def updateFile(current_score):
    f = open("scores_worm.txt", "r")
    file = f.readlines()
    last = int(file[0])

    if last < int(current_score):
        f.close()
        file = open("scores_worm.txt", "w")
        file.write(str(current_score))
        file.close()

        return current_score
    return last


def replay_or_quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        elif event.type == pygame.KEYUP:
            continue

        # door deze elif wordt alleen door een toets gereageerd en niet meer door de muis
        elif event.type == pygame.KEYDOWN:
            return event.key


def endscreen(current_score):
    smallText = pygame.font.Font("freesansbold.ttf", 20)
    mediumText = pygame.font.Font("freesansbold.ttf", 50)
    largeText = pygame.font.Font("freesansbold.ttf", 130)

    gameOverSurface = largeText.render("Game Over", True, durt)
    gameOver_rect = gameOverSurface.get_rect(center=(width / 2, ((height / 2) - 125)))
    screen.blit(gameOverSurface, gameOver_rect)

    textSurface = smallText.render("Press any key to replay", True, durt)
    text_rect = textSurface.get_rect(center=(width / 2, ((height) - 50)))
    screen.blit(textSurface, text_rect)

    lastScore = mediumText.render(
        "Best Score: " + str(updateFile(current_score)), True, durt
    )
    lastScore_rect = lastScore.get_rect(center=(width / 2, ((height / 2) + 70)))
    screen.blit(lastScore, lastScore_rect)

    currentScore = mediumText.render("Score: " + str(current_score), True, durt)
    currentScore_rect = currentScore.get_rect(center=(width / 2, (height / 2)))
    screen.blit(currentScore, currentScore_rect)

    pygame.display.update()
    time.sleep(1)

    while replay_or_quit() is None:
        clock.tick()
    main()


def main():
    worm_speed = 15

    # begin wormpositie
    worm_position = [100, 50]

    # begin lengte van de worm
    worm_body = [[100, 50], [90, 50], [80, 50], [70, 50]]

    # begin fruitpositie
    fruit_position = [
        random.randint(1, (width // 10)) * 10,
        random.randint(1, (height // 10)) * 10,
    ]

    fruit_spawn = True

    direction = "RIGHT"
    change_to = direction

    score = 0

    while True:
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # geeft richting wanneer er een knop wordt ingeduwd, veranderd richting
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = "UP"
                if event.key == pygame.K_DOWN:
                    change_to = "DOWN"
                if event.key == pygame.K_LEFT:
                    change_to = "LEFT"
                if event.key == pygame.K_RIGHT:
                    change_to = "RIGHT"

        # zorgt ervoor dat de worm niet in zichzelf kan keren
        if change_to == "UP" and direction != "DOWN":
            direction = "UP"
        if change_to == "DOWN" and direction != "UP":
            direction = "DOWN"
        if change_to == "LEFT" and direction != "RIGHT":
            direction = "LEFT"
        if change_to == "RIGHT" and direction != "LEFT":
            direction = "RIGHT"

        # laat de worm bewegen
        if direction == "UP":
            worm_position[1] -= 10
        if direction == "DOWN":
            worm_position[1] += 10
        if direction == "LEFT":
            worm_position[0] -= 10
        if direction == "RIGHT":
            worm_position[0] += 10

        # invoegen van de delen van de worm in het lichaam van de worm
        worm_body.insert(0, list(worm_position))

        # aanraking van de worm en fruit
        if (
            worm_position[0] == fruit_position[0]
            and worm_position[1] == fruit_position[1]
        ):
            score += 1
            fruit_spawn = False

        # zorgt dat de worm niet blijft groeien
        else:
            worm_body.pop()

        # terug fruit spawnen als er geen meer is, opgegeten is
        if not fruit_spawn:
            fruit_position = [
                random.randrange(1, (width // 10)) * 10,
                random.randrange(1, (height // 10)) * 10,
            ]

        fruit_spawn = True

        # tekenen van het fruit en de worm
        for pos in worm_body:
            pygame.draw.rect(screen, worm_color, pygame.Rect(pos[0], pos[1], 10, 10))
            pygame.draw.rect(
                screen, red, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10)
            )

        # eindscherm bij aanraking van de randen
        if worm_position[0] < 0 or worm_position[0] > width - 10:
            endscreen(score)
        if worm_position[1] < 0 or worm_position[1] > height - 10:
            endscreen(score)

        # eindscherm bij aanraking van delen van de worms lichaam
        for block in worm_body[1:]:
            if worm_position[0] == block[0] and worm_position[1] == block[1]:
                endscreen(score)

        show_score(score)
        updateFile(score)
        pygame.display.update()
        clock.tick(worm_speed)


main()
