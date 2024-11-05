import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
LANES = 5
LANE_WIDTH = SCREEN_WIDTH // LANES
CAR_WIDTH, CAR_HEIGHT = 50, 100
OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 50, 50
FPS = 60
INITIAL_LIVES = 5
INITIAL_SPAWN_LIMIT = 30
INITIAL_SPEED = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
LIGHT_GREY = (200, 200, 200)
DARK_GREY = (100, 100, 100)

# Setup screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car Test")
clock = pygame.time.Clock()

car_image = pygame.image.load('car.png')
car_image = pygame.transform.scale(car_image, (CAR_WIDTH, CAR_HEIGHT))

obstacle1_image = pygame.image.load('obstacle1.png')
obstacle1_image = pygame.transform.scale(obstacle1_image, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))

font = pygame.font.SysFont(None, 24)
game_over_font = pygame.font.SysFont('arial', 36)  # Larger font for Game Over

# Car class
class Car:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.lane = 2

    def move_left(self):
        if self.lane > 0:
            self.lane -= 1

    def move_right(self):
        if self.lane < 4:
            self.lane += 1

    def draw(self):
        screen.blit(car_image, (self.lane * LANE_WIDTH + (LANE_WIDTH - CAR_WIDTH) // 2, self.y))

# Obstacle class
class Obstacle:
    def __init__(self):
        self.lane = random.randint(0, 4)
        self.y = -100

    def update(self, speed):
        self.y += speed  # Speed of obstacle

    def draw(self):
        screen.blit(obstacle1_image, \
            (self.lane * LANE_WIDTH + (LANE_WIDTH - CAR_WIDTH) // 2, self.y))

# Draw lane dividers
def draw_lane_dividers():
    for i in range(1, 5):
        pygame.draw.line(screen, DARK_GREY, \
            (i * LANE_WIDTH, 0), (i * LANE_WIDTH, SCREEN_HEIGHT), 5)

# Display the score and lives
def display_stats(score, lives):
    score_text = font.render(f"Score: {score}", True, BLACK)
    lives_text = font.render(f"Lives: {lives}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (SCREEN_WIDTH - 150, 10))

# Game Over dialog
def game_over_dialog(score):
    game_over_text = game_over_font.render(f"Game Over! {score} Press Enter to Restart", True, BLACK)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 - 50))
    pygame.display.flip()
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting_for_input = False
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    return True

# Game variables
car = Car(LANE_WIDTH * 2, SCREEN_HEIGHT - 120)
obstacles = []
spawn_counter = 0
score = 0
lives = INITIAL_LIVES
spawn_limit = 30
speed = INITIAL_SPEED
level_ticks = 0

# Game loop
running = True
while running:
    screen.fill(LIGHT_GREY)
    draw_lane_dividers()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                car.move_left()
            if event.key == pygame.K_RIGHT:
                car.move_right()

    # Spawn obstacles
    spawn_counter += 1
    if spawn_counter >= spawn_limit:
        obstacles.append(Obstacle())
        spawn_counter = 0

    # Update and draw obstacles
    for obstacle in obstacles[:]:
        obstacle.update(speed)
        obstacle.draw()
        if obstacle.y > SCREEN_HEIGHT:
            obstacles.remove(obstacle)
        else:
            if obstacle.lane == car.lane and \
               obstacle.y < car.y + CAR_HEIGHT and \
               car.y < obstacle.y + OBSTACLE_HEIGHT:
               lives -= 1
               obstacles.remove(obstacle)
               if lives == 0:
                 if game_over_dialog(score):
                   score = 0
                   lives = INITIAL_LIVES
                   obstacles = []
                   car.lane = 2
                   spawn_limit = INITIAL_SPAWN_LIMIT
                   speed = INITIAL_SPEED
                   continue

    # Draw car
    car.draw()

    # Display score and lives
    display_stats(score, lives)

    # Level Advancement
    score += 1
    level_ticks += 1
    if level_ticks >= 100:
        level_ticks = 0
        speed += 1
        spawn_limit -= 1
        if spawn_limit < 10:
            spawn_limit = 10

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
