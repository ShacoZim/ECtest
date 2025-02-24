import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Egg Catcher")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Basket properties
basket_width = 100
basket_height = 20
basket_x = WIDTH // 2 - basket_width // 2
basket_y = HEIGHT - basket_height - 10
basket_speed = 10

# Egg properties
egg_width = 30
egg_height = 40
egg_speed = 5
egg_drop_frequency = 25  # Higher value means fewer drops

# Initialize variables
score = 0
missed_eggs = 0
eggs = []
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

def draw_text(text, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def draw_basket(x, y):
    pygame.draw.rect(screen, BLACK, [x, y, basket_width, basket_height])

def draw_egg(egg):
    pygame.draw.ellipse(screen, RED, egg)

def move_eggs(eggs):
    for egg in eggs:
        egg['rect'].move_ip(0, egg_speed)

def remove_off_screen_eggs(eggs):
    return [egg for egg in eggs if egg['rect'].top < HEIGHT]

def check_for_catch(eggs, basket_rect):
    global score, missed_eggs
    for egg in eggs:
        if basket_rect.colliderect(egg['rect']):
            score += 1
            eggs.remove(egg)
        elif egg['rect'].top >= HEIGHT:
            missed_eggs += 1
            eggs.remove(egg)

# Game loop
running = True
while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and basket_x - basket_speed > 0:
        basket_x -= basket_speed
    if keys[pygame.K_RIGHT] and basket_x + basket_speed < WIDTH - basket_width:
        basket_x += basket_speed

    if random.randint(1, egg_drop_frequency) == 1:
        egg_x = random.randint(0, WIDTH - egg_width)
        new_egg = {'rect': pygame.Rect(egg_x, 0, egg_width, egg_height)}
        eggs.append(new_egg)

    move_eggs(eggs)
    eggs = remove_off_screen_eggs(eggs)
    basket_rect = pygame.Rect(basket_x, basket_y, basket_width, basket_height)
    check_for_catch(eggs, basket_rect)

    draw_basket(basket_x, basket_y)
    for egg in eggs:
        draw_egg(egg['rect'])

    draw_text(f'Score: {score}', BLACK, 10, 10)
    draw_text(f'Missed: {missed_eggs}', BLACK, 10, 50)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
