import pygame
import random
import time
import sys

pygame.init()

width = 1000
height = 800

white = (255, 255, 255)
green = (0, 250, 0)

screen = pygame.display.set_mode((width, height))

background = pygame.image.load("afbeeldingen/chalkboard.png")
# achtergrond schaal veranderen naar die van het scherm
background = pygame.transform.scale(background, (width, height))

pygame.display.set_caption("Shoot the Teacher")
icon = pygame.image.load("afbeeldingen/school.png")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()


def show_score(score_count):
    font = pygame.font.Font("freesansbold.ttf", 20)
    score = font.render("Score : " + str(score_count), True, white)
    screen.blit(score, (10, 10))


def updateFile(current_score):
    f = open("scores_stt.txt", "r")
    file = f.readlines()
    last = int(file[0])

    if last < int(current_score):
        f.close()
        file = open("scores_stt.txt", "w")
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

    gameOverSurface = largeText.render("Game Over", True, green)
    gameOver_rect = gameOverSurface.get_rect(center=(width / 2, ((height / 2) - 125)))
    screen.blit(gameOverSurface, gameOver_rect)

    textSurface = smallText.render("Press any key to continue", True, green)
    text_rect = textSurface.get_rect(center=(width / 2, ((height) - 50)))
    screen.blit(textSurface, text_rect)

    lastScore = mediumText.render(
        "Best Score: " + str(updateFile(current_score)), True, green
    )
    lastScore_rect = lastScore.get_rect(center=(width / 2, ((height / 2) + 70)))
    screen.blit(lastScore, lastScore_rect)

    currentScore = mediumText.render("Score: " + str(current_score), True, green)
    currentScore_rect = currentScore.get_rect(center=(width / 2, (height / 2)))
    screen.blit(currentScore, currentScore_rect)

    pygame.display.update()
    time.sleep(1)

    while replay_or_quit() is None:
        clock.tick()
    main()


def fire_book():
    global book_state
    book_state = "fire"


def main():
    groep = pygame.sprite.Group()
    # student
    student_move = 0
    student_sprite = pygame.sprite.Sprite()
    student_sprite.image = pygame.image.load("afbeeldingen/student.png")
    student_sprite.rect = student_sprite.image.get_rect()
    student_sprite.rect.center = (450, 700)
    groep.add(student_sprite)

    # teacher
    teacherlist = []
    teacher_move = []
    number_of_teachers = 6

    for i in range(number_of_teachers):
        teacher_sprite = pygame.sprite.Sprite()
        teacher_sprite.image = pygame.image.load("afbeeldingen/teacher.png")
        teacher_sprite.rect = teacher_sprite.image.get_rect()
        teacher_sprite.rect.center = (random.randint(0, 908), 50)
        teacherlist.append(teacher_sprite)
        teacher_move.append(1)
        groep.add(teacher_sprite)

    # book
    # ready - het book is klaar om geworpen te worden
    # fire - het book is in beweging
    book_state = "ready"
    book = pygame.sprite.Sprite()
    book.image = pygame.image.load("afbeeldingen/book.png")
    book.rect = book.image.get_rect()
    book.rect.center = (student_sprite.rect.x + 15, student_sprite.rect.y + 37)
    groep.add(book)

    # score
    score_count = 0

    while True:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        groep.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # bewegen student
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    student_move = -2
                if event.key == pygame.K_RIGHT:
                    student_move = 2

                # boek laten bewegen bij indrukken spatie
                if event.key == pygame.K_SPACE:
                    # de if functie dient zodat het boek niet verplaatst met de student na het vuren en drukken op spatie
                    if book_state == "ready":
                        # de x-coördinaat van het boek gelijk stellen aan die van de student zodat het boek niet meeverplaatst met de student maar op de x-coördinaat blijft van het afvuren
                        book.rect.center = (
                            student_sprite.rect.x + 15,
                            student_sprite.rect.y + 37,
                        )
                        book_state = "fire"

            # stoppen met bewegen bij loslaten van de toetsen
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    student_move = 0

        student_sprite.rect.x += student_move

        # grenzen student
        if student_sprite.rect.left <= 0:
            # kan niet verder dan grenswaarde bewegen
            student_sprite.rect.left = 0
        elif student_sprite.rect.right >= 918:
            # kan niet verder dan grenswaarde bewegen
            student_sprite.rect.right = 918

        for i in range(number_of_teachers):
            # grens waar leraren niet over kunnen bij de student, bij aanraking -> eindscherm
            if teacherlist[i].rect.y > 600:
                endscreen(score_count)
            # beweging leeraar
            teacherlist[i].rect.x += teacher_move[i]

            # grenzen leeraar
            if teacherlist[i].rect.left <= 0:
                # andere richting bij berijken van grenswaarde
                teacher_move[i] = 1
                # laten zakken bij grenzen
                teacherlist[i].rect.y += 80
            elif teacherlist[i].rect.right >= 908:
                # andere richting bij berijken van grenswaarde
                teacher_move[i] = -1
                # laten zakken bij grenzen
                teacherlist[i].rect.y += 80

            # aanraking van het boek met een van de leraren
            if teacherlist[i].rect.collidepoint(book.rect.center):
                teacherlist[i].rect.center = (random.randint(0, 908), 50)
                score_count += 1
                book_state = "ready"

            # bij aanraken van de student en een van de leraren direct naar eindscherm (is uit voorzorg, want de leraren geraken niet aan de student door de grens van eerder)
            if student_sprite.rect.collidepoint(teacherlist[i].rect.center):
                endscreen(score_count)

        # boek terug ready bij aanraking bovenaan scherm
        if book.rect.top <= 0:
            book.rect.y = 650
            book_state = "ready"

        # beweging boek
        if book_state == "fire":
            fire_book()
            book.rect.y -= 1

        # boek na vuren terug plaatsen in de handen van de student
        if book_state == "ready":
            book.rect.center = (student_sprite.rect.x + 15, student_sprite.rect.y + 37)

        show_score(score_count)
        updateFile(score_count)
        pygame.display.update()


main()
