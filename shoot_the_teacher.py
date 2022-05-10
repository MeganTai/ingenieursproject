import pygame
import random

pygame.init()

screen = pygame.display.set_mode((1000, 800))

background = pygame.image.load("afbeeldingen/chalkboard.png")
# achtergrond schaal veranderen naar die van het scherm
background = pygame.transform.scale(background, (1000, 800))

pygame.display.set_caption("Shoot the Teacher")
icon = pygame.image.load("afbeeldingen/school.png")
pygame.display.set_icon(icon)

# student
studentImage = pygame.image.load("afbeeldingen/student.png")
studentX = 450
studentY = 650
studentX_move = 0

# teacher
teacherImage = pygame.image.load("afbeeldingen/teacher.png")
teacherX = random.randint(0, 908)
teacherY = random.randint(50, 50)
teacherX_move = 0.4
teacherY_move = 80

# book
bookImage = pygame.image.load("afbeeldingen/book.png")
bookX = 0
bookY = 650
bookX_move = 0
bookY_move = 1
book_state = "ready"


def student(x, y):
    screen.blit(studentImage, (x, y))


def teacher(x, y):
    screen.blit(teacherImage, (x, y))


def fire_book(x, y):
    global book_state
    book_state = "fire"
    # + en - om positie bij start te speciferen
    screen.blit(bookImage, (x - 2, y + 21))


running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # bewegen student
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                studentX_move = -0.5
            if event.key == pygame.K_RIGHT:
                studentX_move = 0.5

            # boek laten bewegen bij indrukken spatie
            if event.key == pygame.K_SPACE:
                # de if functie dient zodat het boek niet verplaatst met de student na het vuren en drukken op spatie
                if book_state is "ready":
                    # de x-coördinaat van het boek gelijk stellen aan die van de student zodat het boek niet meeverplaatst met de student maar op de x-coördinaat blijft van het afvuren
                    bookX = studentX
                    fire_book(bookX, bookY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                studentX_move = 0

    studentX += studentX_move

    # grenzen student
    if studentX <= 0:
        # kan niet verder dan grenswaarde bewegen
        studentX = 0
    elif studentX >= 918:
        # kan niet verder dan grenswaarde bewegen
        studentX = 918

    # beweging leeraar
    teacherX += teacherX_move

    # grenzen leeraar
    if teacherX <= 0:
        # andere richting bij berijken van grenswaarde
        teacherX_move = 0.4
        # laten zakken bij grenzen
        teacherY += teacherY_move
    elif teacherX >= 908:
        # andere richting bij berijken van grenswaarde
        teacherX_move = -0.4
        # laten zakken bij grenzen
        teacherY += teacherY_move

    # beweging boek
    if bookY <= 0:
        bookY = 650
        book_state = "ready"
    if book_state is "fire":
        fire_book(bookX, bookY)
        bookY -= bookY_move

    student(studentX, studentY)
    teacher(teacherX, teacherY)
    pygame.display.update()
