from math import hypot
from random import randint
import pygame

#налаштування гри
WIDTH = 1000          #ширина вікна
HEIGHT = 1000         #висота вікна
FOOD_COUNT = 1000     #скільки кружечків-їжі буде на полі
WORLD_SIZE = 4000     #де можуть з'явитися кружечки (від -4000 до 4000)
PLAYER_SPEED = 15     #швидкість руху гравця
FPS = 60              #скільки кадрів за секунду

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("З'їж кружечки!")
clock = pygame.time.Clock()

#Гравець
player_x = 0
player_y = 0
player_radius = 20
player_color = (0, 255, 0)  # зелений







def move_player():
    player = pygame.key.get_pressed()
    if player[pygame.K_UP]:
        player.y -= PLAYER_SPEED
    if player[pygame.K_DOWN]:
        player.y += PLAYER_SPEED
    if player[pygame.K_LEFT]:
        player.x -= PLAYER_SPEED
    if player[pygame.K_RIGHT]:
        player.x += PLAYER_SPEED

def world_to_screen(x, y, scale):
    b_x = x - player_x
    b_y = y - player_y
    h_x = b_x * scale
    h_y = b_y * scale
    halfx = WIDTH // 2
    halfy = HEIGHT // 2
    screen_x = h_x + halfx
    screen_y = h_y + halfy
    return screen_x, screen_y





#головний цикл гри
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    move_player(keys)
    eat_food()
    draw_everything()

    clock.tick(FPS)
    pygame.display.flip()

pygame.quit()
