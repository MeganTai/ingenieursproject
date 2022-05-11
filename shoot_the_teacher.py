from email.mime import image
import pygame
import random
import math
import time

pygame.init()

width = 1000
height = 800
white = (255, 255, 255)

screen = pygame.display.set_mode((width, height))

background = pygame.image.load("afbeeldingen/chalkboard.png")
# achtergrond schaal veranderen naar die van het scherm
background = pygame.transform.scale(background, (width, height))

pygame.display.set_caption("Shoot the Teacher")
icon = pygame.image.load("afbeeldingen/school.png")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()


def show_score(x, y, score_count):
    font = pygame.font.Font("freesansbold.ttf", 20)
    score = font.render("Score : " + str(score_count), True, (255, 255, 255))
    screen.blit(score, (x, y))


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

    gameOverSurface = largeText.render("Gamer Over", True, white)
    gameOver_rect = gameOverSurface.get_rect(center=(width / 2, ((height / 2) - 125)))
    screen.blit(gameOverSurface, gameOver_rect)

    textSurface = smallText.render("Press any key to continue", True, white)
    text_rect = textSurface.get_rect(center=(width / 2, ((height) - 50)))
    screen.blit(textSurface, text_rect)

    lastScore = mediumText.render(
        "Best Score: " + str(updateFile(current_score)), True, white
    )
    lastScore_rect = lastScore.get_rect(center=(width / 2, ((height / 2) + 70)))
    screen.blit(lastScore, lastScore_rect)

    currentScore = mediumText.render("Score: " + str(current_score), True, white)
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
    student_sprite.rect.center = (450, 650)
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
    book_state = "ready"
    book = pygame.sprite.Sprite()
    book.image = pygame.image.load("afbeeldingen/book.png")
    book.rect = book.image.get_rect()
    book.rect.center = (0, 650)
    groep.add(book)

    # score
    score_count = 0

    textX = 10
    textY = 10
    
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
                    student_move = -1
                if event.key == pygame.K_RIGHT:
                    student_move = 1
            

                # boek laten bewegen bij indrukken spatie
                if event.key == pygame.K_SPACE:
                    # de if functie dient zodat het boek niet verplaatst met de student na het vuren en drukken op spatie
                    if book_state == "ready":
                        # de x-coördinaat van het boek gelijk stellen aan die van de student zodat het boek niet meeverplaatst met de student maar op de x-coördinaat blijft van het afvuren
                        book.rect.x = student_sprite.rect.x - 2
                        book.rect.y += 21
                        book_state = "fire"
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
            if teacherlist[i].rect.y > 700:
                for j in groep:
                    groep.remove(j)
                endscreen(score_count)
                break
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

            
            if teacherlist[i].rect.collidepoint(book.rect.center):
                teacherlist[i].rect.center = (random.randint(0, 908),50)
                score_count += 1
                book.rect.center = (student_sprite.rect.x - 2, student_sprite.rect.y + 21)
                book_state = "ready"

        # beweging boek
        if book.rect.top <= 0:
            book.rect.y = 650
            book_state = "ready"

        if book_state == "fire":
            fire_book()
            book.rect.y -= 1

        show_score(textX, textY, score_count)
        updateFile(score_count)
        pygame.display.update()


main()
pygame.quit()
quit()
