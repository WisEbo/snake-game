import pygame
import random
import time

pygame.init()

""" game screen display size and cell size """
screen_width, screen_height = 800, 600
cell_size = 20

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")

""" Set up the clock for a decent framerate"""
clock = pygame.time.Clock()
frames_per_second = 10

""" Place the snake in a straight line in the center """
snake_position = [
    [screen_width // 2, screen_height // 2],              # Head
    [screen_width // 2 - cell_size, screen_height // 2],  # Segment 1
    [screen_width // 2 - 2 * cell_size, screen_height // 2]  # Segment 2
]

print("Starting snake position:", snake_position)

snake_direction = 'RIGHT'

new_direction = snake_direction


def spawn_food(snake_position):
    while True:
        food_pos = [random.randrange(1, screen_width // cell_size) * cell_size,
                    random.randrange(1, screen_height // cell_size) * cell_size]
        if food_pos not in snake_position:
            return food_pos

""" Initial snake food position """
food_pos = spawn_food(snake_position)
food_spawn = True


print("Initial snake position:", snake_position)
print("Initial food position:", food_pos)

""" Game over logic """
def game_over():
    font = pygame.font.SysFont('arial', 50)
    go_surface = font.render('Game Over', True, red)
    go_rect = go_surface.get_rect()
    go_rect.midtop = (screen_width / 2, screen_height / 4)
    screen.fill(black)
    screen.blit(go_surface, go_rect)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    quit()


""" Main game loop """
score = 0

while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_direction != 'DOWN':
                new_direction = 'UP'
            elif event.key == pygame.K_DOWN and snake_direction != 'UP':
                new_direction = 'DOWN'
            elif event.key == pygame.K_LEFT and snake_direction != 'RIGHT':
                new_direction = 'LEFT'
            elif event.key == pygame.K_RIGHT and snake_direction != 'LEFT':
                new_direction = 'RIGHT'
        elif event.type == pygame.QUIT:
            pygame.quit()
            quit()

    """ Update the direction of the snake """
    snake_direction = new_direction
    
    """ Move the snake: create a new head position based on new direction """
    if snake_direction == 'UP':
        new_head = [snake_position[0][0], snake_position[0][1] - cell_size]
    elif snake_direction == 'DOWN':
        new_head = [snake_position[0][0], snake_position[0][1] + cell_size]
    elif snake_direction == 'LEFT':
        new_head = [snake_position[0][0] - cell_size, snake_position[0][1]]
    elif snake_direction == 'RIGHT':
        new_head = [snake_position[0][0] + cell_size, snake_position[0][1]]

    """ Insert the new head at the beginning of snake_position """
    snake_position.insert(0, new_head)
    
    """ Check if the snake has eaten the food """
    if snake_position[0] == food_pos:
        score += 1
        food_spawn = False  # This will trigger new food placement
    else:
        snake_position.pop()
    
    """ Spawn new food if needed """
    if not food_spawn:
        food_pos = spawn_food(snake_position)
        food_spawn = True

    print("Snake position:", snake_position)
    print("Food position:", food_pos)
    
    """ Wall collision check """
    if snake_position[0][0] < 0 or snake_position[0][0] >= screen_width or \
       snake_position[0][1] < 0 or snake_position[0][1] >= screen_height:
        print(f"Wall collision at {snake_position[0]}")
        game_over()
    
    """ Self-collision check """
    for block in snake_position[1:]:
        if snake_position[0] == block:
            print(f"Self-collision detected at {snake_position[0]}")
            game_over()
    
    """ Clear the screen """
    screen.fill(black)  
    
    """ Draw the snake """
    for pos in snake_position:
        pygame.draw.rect(screen, green, pygame.Rect(pos[0], pos[1], cell_size, cell_size))
    
    """ Draw the food """
    pygame.draw.rect(screen, red, pygame.Rect(food_pos[0], food_pos[1], cell_size, cell_size))
    
    """ Display the score """
    font = pygame.font.SysFont('arial', 35)
    score_surface = font.render('Score: ' + str(score), True, white)
    score_rect = score_surface.get_rect()
    score_rect.midtop = (screen_width / 2, 15)
    screen.blit(score_surface, score_rect)

    """ Refresh game screen """
    pygame.display.update()

    """ Control the game speed """
    clock.tick(frames_per_second)
