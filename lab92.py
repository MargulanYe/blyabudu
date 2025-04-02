import pygame
import random
time = pygame.time

pygame.init()

WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

snake = [(100, 100), (90, 100), (80, 100)]
direction = (CELL_SIZE, 0)

def generate_food():
    while True:
        x = random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE
        y = random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
        if (x, y) not in snake:
            return x, y

food = generate_food()
food_timer = time.get_ticks() 
score = 0
level = 1
speed = 10

running = True
while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                direction = (0, -CELL_SIZE)
            elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                direction = (0, CELL_SIZE)
            elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                direction = (-CELL_SIZE, 0)
            elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                direction = (CELL_SIZE, 0)

    new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

    if (new_head[0] < 0 or new_head[0] >= WIDTH or
        new_head[1] < 0 or new_head[1] >= HEIGHT or
        new_head in snake):
        running = False

    snake.insert(0, new_head)

    if new_head == food:
        score += random.randint(1, 5)
        food = generate_food()
        food_timer = time.get_ticks()
        if score % 3 == 0:
            level += 1
            speed += 2
    else:
        snake.pop()
    if time.get_ticks() - food_timer > 10000:
        food = generate_food()
        food_timer = time.get_ticks() 

    pygame.draw.rect(screen, RED, (*food, CELL_SIZE, CELL_SIZE))

    for segment in snake:
        pygame.draw.rect(screen, BLUE, (*segment, CELL_SIZE, CELL_SIZE))

    font = pygame.font.SysFont(None, 30)
    score_text = font.render(f"Score: {score}  Level: {level}", True, GREEN)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()
