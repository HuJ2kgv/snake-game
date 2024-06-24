import pygame
import time
import random

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
boost_color = (255, 255, 0)  # Yellow for boost bar

# Clock
clock = pygame.time.Clock()
snake_speed = 7.5
boost_speed = 15
boost_duration = 100  # Boost duration in frames
boost_cooldown = 200  # Cooldown duration in frames
current_boost = boost_duration
boost_recharge = boost_cooldown

# Snake block size
block_size = 20

# Fonts
font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)

def our_snake(block_size, snake_list):
    for block in snake_list:
        pygame.draw.rect(display, black, [block[0], block[1], block_size, block_size])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    display.blit(mesg, [width / 6, height / 3])

def draw_boost_bar(current_boost, boost_duration, boost_recharge, boost_cooldown):
    boost_bar_width = width * (current_boost / boost_duration)
    boost_bar_height = 20
    boost_bar_x = 0
    boost_bar_y = 0
    pygame.draw.rect(display, boost_color, [boost_bar_x, boost_bar_y, boost_bar_width, boost_bar_height])

    # Draw cooldown bar if boost is not fully recharged
    if boost_recharge > 0:
        cooldown_bar_width = width * (boost_recharge / boost_cooldown)
        cooldown_bar_x = width - cooldown_bar_width
        cooldown_bar_y = 0
        pygame.draw.rect(display, black, [cooldown_bar_x, cooldown_bar_y, cooldown_bar_width, boost_bar_height])

    # Display cooldown timer if applicable
    if boost_recharge > 0:
        cooldown_timer_text = score_font.render(f"{boost_recharge // snake_speed}", True, white)
        display.blit(cooldown_timer_text, (width - cooldown_timer_text.get_width() - 10, 5))

def gameLoop():
    game_over = False
    game_close = False

    x1 = width / 2
    y1 = height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, width - block_size) / block_size) * block_size
    foody = round(random.randrange(0, height - block_size) / block_size) * block_size

    global current_boost, boost_recharge

    while not game_over:

        while game_close == True:
            display.fill(blue)
            message("You Lost! Press Q-Quit or C-Play Again", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    x1_change = -block_size
                    y1_change = 0
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    x1_change = block_size
                    y1_change = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    y1_change = -block_size
                    x1_change = 0
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    y1_change = block_size
                    x1_change = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            if current_boost > 0:
                current_speed = boost_speed
                current_boost -= 1
            else:
                current_speed = snake_speed
                if boost_recharge > 0:
                    boost_recharge -= 1
                else:
                    current_boost = boost_duration
                    boost_recharge = boost_cooldown
        else:
            current_speed = snake_speed
            if current_boost < boost_duration:
                if boost_recharge > 0:
                    boost_recharge -= 1
                else:
                    current_boost += 1

        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        display.fill(blue)

        # Draw the boost bar and cooldown timer
        draw_boost_bar(current_boost, boost_duration, boost_recharge, boost_cooldown)

        pygame.draw.rect(display, green, [foodx, foody, block_size, block_size])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for block in snake_List[:-1]:
            if block == snake_Head:
                game_close = True

        our_snake(block_size, snake_List)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - block_size) / block_size) * block_size
            foody = round(random.randrange(0, height - block_size) / block_size) * block_size
            Length_of_snake += 1

        clock.tick(current_speed)  # Use the current speed for the clock

    pygame.quit()
    quit()

gameLoop()
