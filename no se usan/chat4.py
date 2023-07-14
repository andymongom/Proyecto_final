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

def win_message():
    win_text = win_font.render("YOU WIN", True, (255, 255, 255))
    SCREEN.blit(win_text, (200, 200))

def niveles_meteoritos():
    # Player variables
    img_player = pygame.image.load("icons8-star-wars-naboo-ship-64.png")
    player_x = 368  # 400 - 32 para que quede centrado
    player_y = 536  # 600- 64 para que quede centrado
    player_x_change = 0

    # Enemy variables
    img_enemy = []
    enemy_x = []
    enemy_y = []
    enemy_x_change = []
    enemy_y_change = []
    number_of_enemies = 10
    velocidad_enemigos = 1.8  # Velocidad inicial de los enemigos
    velocidad_enemigos_global = velocidad_enemigos  # Velocidad global de los enemigos
    factor_aumento_velocidad = 1.1  # Factor de aumento de velocidad

    for i in range(number_of_enemies):
        img_enemy.append(pygame.image.load("icons8-star-trek-romulan-ship-64.png"))
        enemy_x.append(random.randint(0, 736))
        enemy_y.append(random.randint(30, 200))
        enemy_x_change.append(velocidad_enemigos)
        enemy_y_change.append(1.8)

    # Bullet variables
    img_bullet = pygame.image.load("icons8-rayo-láser-32.png")
    bullet_x = 0
    bullet_y = 0
    bullet_x_change = 0
    bullet_y_change = 15
    bullet_visible = False

    # Score Variables
    score = 0
    score_font = pygame.font.Font("freesansbold.ttf", 32)
    score_text_x = 10
    score_text_y = 10

    # Level Variable
    nivel = 1

    # Meteor variables
    img_meteorito = pygame.image.load("asteroid_98597.png")
    meteorito_x = []
    meteorito_y = []
    meteorito_visible = False

    # Show score
    def show_score(x, y):
        text = score_font.render(f"Score: {score}", True, (255, 255, 255))
        SCREEN.blit(text, (x, y))

    # Show level
    def show_level(x, y):
        level_text = score_font.render(f"Level: {nivel}", True, (255, 255, 255))
        SCREEN.blit(level_text, (x, y + 50))

    # Show meteoritos
    def show_meteoritos():
        if meteorito_visible:
            for i in range(len(meteorito_x)):
                meteorito_y[i] += 5  # Ajusta la velocidad de caída de los meteoritos
                SCREEN.blit(img_meteorito, (meteorito_x[i], meteorito_y[i]))
                if meteorito_y[i] > 600:
                    # Eliminar el meteorito si sale de la pantalla
                    meteorito_x.pop(i)
                    meteorito_y.pop(i)
                    break

            # Crear nuevos meteoritos
            if len(meteorito_x) < 10:  # Número máximo de meteoritos en pantalla
                meteorito_x.append(random.randint(50, 750))
                meteorito_y.append(random.randint(-200, -50))

    # Show player in screen
    def player(x, y):
        SCREEN.blit(img_player, (x, y))

    # Show enemy
    def enemy(x, y, enemy_index):
        SCREEN.blit(img_enemy[enemy_index], (x, y))

    # Shoot Bullet
    def shoot_bullet(x, y):
        nonlocal bullet_visible
        bullet_visible = True
        SCREEN.blit(img_bullet, (x + 16, y + 10))

    # Detect collision
    def detect_collision(x_1, y_1, x_2, y_2):
        x_sub = x_2 - x_1
        y_sub = y_2 - y_1
        distance = math.sqrt(math.pow(x_sub, 2) + math.pow(y_sub, 2))
        if distance < 27:
            return True

    # Game loop
    is_running = True
    while is_running:
        # Image background
        SCREEN.blit(BG, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_x_change -= 7.0
                if event.key == pygame.K_RIGHT:
                    player_x_change += 7.0
                if event.key == pygame.K_SPACE:
                    if not bullet_visible:
                        bullet_x = player_x
                    shoot_bullet(bullet_x, bullet_y)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                    player_x_change = 0

        # Update player location
        player_x += player_x_change

        # Keep player inside the screen
        if player_x <= 0:
            player_x = 0
        elif player_x >= 736:
            player_x = 736

        for i in range(number_of_enemies):
            # Update enemy location
            enemy_x[i] += velocidad_enemigos_global * enemy_x_change[i]

            # Keep enemies inside the screen
            if enemy_x[i] <= 0:
                enemy_x_change[i] += 0.3
                enemy_y[i] += enemy_y_change[i]
            elif enemy_x[i] >= 736:
                enemy_x_change[i] -= 0.3
                enemy_y[i] += enemy_y_change[i]

            # Detect collision
            collision = detect_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
            if collision:
                enemy_x[i] = random.randint(0, 736)
                enemy_y[i] = random.randint(30, 200)
                bullet_visible = False
                score += 1
                bullet_y = 500

                if score % 10 == 0:
                    nivel += 1
                    velocidad_enemigos_global *= factor_aumento_velocidad

            if score == 50 or nivel == 5:
                for j in range(number_of_enemies):
                    enemy_y[j] = 1000
                meteorito_visible = False
                if score == 50:
                    win_message()
                else:
                    final_message()
                is_running = False
                break

            # Show enemy
            enemy(enemy_x[i], enemy_y[i], i)

        # Shoot bullet
        if bullet_y <= -64:
            bullet_y = 500
            bullet_visible = False
        if bullet_visible:
            shoot_bullet(bullet_x, bullet_y)
            bullet_y -= bullet_y_change

        # Show player
        player(player_x, player_y)

        # Show score
        show_score(score_text_x, score_text_y)

        # Show level
        show_level(score_text_x, score_text_y)

        # Show meteoritos
        show_meteoritos()

        # Update screen
        pygame.display.update()

niveles_meteoritos()
pygame.quit()
