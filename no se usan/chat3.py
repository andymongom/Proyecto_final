import pygame
import random
import math

pygame.init()

# Screen
SCREEN = pygame.display.set_mode((800, 600))

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

# Background
BG = pygame.image.load("pexels-francesco-ungaro-998641.jpg")
end_font = pygame.font.Font("assets/font.ttf", 64)
win_font = pygame.font.Font("assets/font.ttf", 64)

def final_message():
    final_text = end_font.render(f"GAME OVER", True, (255, 255, 255))
    SCREEN.blit(final_text, (200, 200))


niveles_meteoritos()
pygame.quit()
