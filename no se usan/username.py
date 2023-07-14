import pygame
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BG_COLOR = (0, 0, 0)
TEXT_COLOR = (255, 255, 255)
FONT_SIZE = 45

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Usernames")

def add_new_user():
    new_username = ""
    base_font = pygame.font.Font(None, FONT_SIZE)

    while True:
        screen.fill(BG_COLOR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Guardar el nombre de usuario en un archivo de texto
                    with open("username", "a") as file:
                        file.write(new_username + "\n")
                    print("New Username:", new_username)
                    return
                elif event.key == pygame.K_BACKSPACE:
                    new_username = new_username[:-1]
                else:
                    new_username += event.unicode

        text_surface = base_font.render("Enter username: " + new_username, True, TEXT_COLOR)
        screen.blit(text_surface, (260, 200))
        pygame.display.update()

add_new_user()
