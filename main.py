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


class Food:
    def __init__(self, x, y, radius, color):

        self.x = x
        self.y = y
        self.radius = radius
        self.color = color




def calculate_camera_scale():
    comfortble_scale = 1.0
    threshold_radius = 100
    zoom_out_speed = 0.8

    if player_radius <= threshold_radius:
        return comfortble_scale

    else:
        a = threshold_radius / player_radius
        b = a ** zoom_out_speed
        return b  
def calculate_food_scale():
    comfortble_scale = 1.0
    threshold_radius = 100
    zoom_out_speed = 0.3

    if player_radius <= threshold_radius:
        return comfortble_scale

    else:
        a = threshold_radius / player_radius
        b = a ** zoom_out_speed
        return b  
    def is_touching_player(self,  px, py, p_radius):

        distance_x = self.x - px
        distance_y = self.y - py
        d = hypot(distance_x , distance_y)
        
        return d <= self.radius + p_radius




def eat_food():
    
    eaten = []
    
    for food in food_items:
        if food.check_collision(player_x, player_y, player_radius):
            eaten.append(food)         
            player_radius += 1          
            
    for food in eaten:
        food_items.remove(food)
        
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
    
def draw_everything():
    window.fill("white")
    camera_scale = calculate_camera_scale()
    food_scale = calculate_food_scale()
    for food in food_items:
        sx,sy = world_to_screen(food.x,food.y,camera_scale)
        scaled_radius = max(1,int(food.radius * food_scale))
        pygame.draw.circle(window,food.color,(sx,sy),scaled_radius)
    scaled_player_radius = int(player_radius * camera_scale)
    pygame.draw.circle(window,player_color,(WIDTH // 2,HEIGHT // 2),scaled_player_radius)




#головний цикл гри
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

from pygame import*
from random import*

arta= food_items
FOOD_COUNT = 1000

def create_food_field():
    food_list = []
    
    for _ in range(FOOD_COUNT):
        x = randint(-WORLD_SIZE, WORLD_SIZE)
        
        y = randint(-WORLD_SIZE, WORLD_SIZE)
        
        color = (randint(0, 255), randint(0, 255), randint(0, 255))

        new_food = Food(x, y, color)
        
   
        food_list.append(new_food)

def playeris_touching(self, other_x, other_y, other_radius):

    distance_x = self.x - self.orher_x
    distance_y = self.y - self.orher_y
    distance = hypot(distance_x, distance_y)

    return distance <= self.radius + other_radius
        
 
    return food_list    
    move_player(keys)
    eat_food()
    draw_everything()

    clock.tick(FPS)
    pygame.display.flip()

pygame.quit()
