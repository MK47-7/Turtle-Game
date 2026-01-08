import pygame
import random
import sys

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
WIDTH, HEIGHT = 600, 700
WHITE = (255, 255, 255)
FPS = 60
FIREBALL_SPEED = 5
TURTLE_SPEED = 7

# Load assets
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Turtle Dodge")
turtle_img = pygame.image.load("turtle.png")
fireball_img = pygame.image.load("fireball.png")

# Resize images
turtle_img = pygame.transform.scale(turtle_img, (80, 80))
fireball_img = pygame.transform.scale(fireball_img, (50, 80))

# Fonts
font = pygame.font.SysFont("Arial", 40)

def draw_text(text, size, color, x, y):
    font = pygame.font.SysFont("Arial", size)
    render = font.render(text, True, color)
    screen.blit(render, (x, y))

def game_over_screen():
    screen.fill((0, 0, 0))
    draw_text("Game Over!", 60, WHITE, WIDTH//2 - 150, HEIGHT//2 - 100)
    draw_text("Press R to Replay", 40, WHITE, WIDTH//2 - 140, HEIGHT//2)
    draw_text("Press Q to Quit", 40, WHITE, WIDTH//2 - 130, HEIGHT//2 + 60)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main_game()
                if event.key == pygame.K_q:
                    pygame.quit(); sys.exit()

def main_game():
    # Restart music when the game starts
    pygame.mixer.music.load("gamemusic.mp3")
    pygame.mixer.music.play(-1)

    clock = pygame.time.Clock()
    turtle_rect = turtle_img.get_rect(center=(WIDTH//2, HEIGHT - 80))
    fireballs = []
    score = 0

    running = True
    while running:
        clock.tick(FPS)
        screen.fill((30, 30, 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and turtle_rect.left > 0:
            turtle_rect.x -= TURTLE_SPEED
        if keys[pygame.K_RIGHT] and turtle_rect.right < WIDTH:
            turtle_rect.x += TURTLE_SPEED

        # Spawn fireballs
        if random.randint(1, 30) == 1:
            x_pos = random.randint(0, WIDTH - 50)
            fireballs.append(fireball_img.get_rect(topleft=(x_pos, -50)))

        # Move fireballs
        for fireball in fireballs:
            fireball.y += FIREBALL_SPEED

            # Shrink collision rectangle for accuracy
            fireball_collision = fireball.inflate(-20, -30)
            turtle_collision = turtle_rect.inflate(-20, -20)

            if fireball_collision.colliderect(turtle_collision):
                pygame.mixer.music.stop()
                game_over_screen()

            screen.blit(fireball_img, fireball)

        screen.blit(turtle_img, turtle_rect)
        draw_text(f"Score: {score}", 30, WHITE, 10, 10)
        score += 1
        pygame.display.flip()

# Start the game
main_game()
