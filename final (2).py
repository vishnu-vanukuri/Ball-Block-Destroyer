import pygame
import time

pygame.init()

# Screen setup
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Image and Sound Demo")
clock = pygame.time.Clock()

# Load assets
player_img = pygame.image.load("finalpic-removebg-preview.png")
player_img = pygame.transform.scale(player_img, (50, 50))

# Load sounds
pygame.mixer.init()
#jump_sound = pygame.mixer.Sound("jump.wav")  # Make sure you have a jump.wav file

# Load the tile image
tile_img = pygame.image.load("tile.png")  # Replace with your tile image path
tile_width, tile_height = tile_img.get_width(), tile_img.get_height()

# Player variables
player_x, player_y = 100, 300
speed = 5
gravity = 0.5
velocity_y = 0
is_jumping = False
ground_y = 300  # The y position that represents the ground

# Trial settings: 10 seconds trial period
trial_start_time = time.time()
trial_duration = 1000  # seconds

running = True
while running:
    # Draw the tiled background
    for y in range(0, 400, tile_height):
        for x in range(0, 600, tile_width):
            screen.blit(tile_img, (x, y))

    # Check if trial time has ended
    if time.time() - trial_start_time > trial_duration:
        font = pygame.font.SysFont(None, 55)
        text = font.render("Trial Time Expired", True, (255, 0, 0))
        screen.blit(text, (150, 150))
        pygame.display.update()
        time.sleep(2)
        running = False
        continue

    # Key input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= speed
    if keys[pygame.K_RIGHT]:
        player_x += speed
    if keys[pygame.K_UP]:
        player_y -= speed  # Move up (optional, for ladders or flying)
    if keys[pygame.K_DOWN]:
        player_y += speed  # Move down (optional)
    if keys[pygame.K_SPACE]:
        if not is_jumping:  # Only jump if not already jumping
            velocity_y = -10  # Jump strength
            is_jumping = True
            jump_sound.play()

    # Gravity and jump logic
    if is_jumping:
        player_y += velocity_y
        velocity_y += gravity
        if player_y >= ground_y:
            player_y = ground_y
            is_jumping = False
            velocity_y = 0

    # Draw player
    screen.blit(player_img, (player_x, player_y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
    clock.tick(60)

pygame.quit()
