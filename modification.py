import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Coin Collector")

# Colors
SKYBLUE = (135, 206, 235)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Clock and FPS
clock = pygame.time.Clock()
FPS = 60

# Font
font = pygame.font.SysFont(None, 36)

# Game settings
player_size = 40
coin_size = 20
enemy_size = 40
gravity = 0.8
jump_power = -15
max_levels = 100
ground_height = 50

# Load and scale player image
player_img = pygame.image.load("player.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (player_size, player_size))

def draw_cloud(x, y):
    pygame.draw.circle(screen, WHITE, (x, y), 20)
    pygame.draw.circle(screen, WHITE, (x + 20, y - 10), 25)
    pygame.draw.circle(screen, WHITE, (x + 40, y), 20)

def create_level(level_num):
    platforms = [pygame.Rect(0, HEIGHT - ground_height, WIDTH, ground_height)]
    for _ in range(min(5 + level_num // 2, 15)):
        x = random.randint(50, WIDTH - 100)
        y = random.randint(100, HEIGHT - 100)
        width = random.randint(100, 150)
        platforms.append(pygame.Rect(x, y, width, 10))

    coins = []
    for platform in platforms[1:]:
        if random.random() < 0.8:
            cx = platform.x + platform.width // 2
            cy = platform.y - coin_size // 2
            coins.append(pygame.Rect(cx, cy, coin_size, coin_size))

    enemies = []
    for platform in platforms[1:]:
        if random.random() < 0.5:
            ex = platform.x + 10
            ey = platform.y - enemy_size
            enemies.append(pygame.Rect(ex, ey, enemy_size, enemy_size))

    enemy_vel = min(2 + level_num * 0.1, 6)
    endpoint = pygame.Rect(WIDTH - 60, platforms[0].y - 40, 40, 40)
    return platforms, coins, enemies, enemy_vel, endpoint

def reset_game(level):
    player_x, player_y = 50, HEIGHT - player_size - ground_height
    player = pygame.Rect(player_x, player_y, player_size, player_size)
    player_vel_x = 0
    player_vel_y = 0
    on_ground = False
    platforms, coins, enemies, enemy_vel, endpoint = create_level(level)
    score = 0
    game_over = False
    game_win = False
    return (player, player_vel_x, player_vel_y, on_ground, platforms,
            coins, enemies, enemy_vel, endpoint, score, game_over, game_win)

# Start the first level
current_level = 1
(player, player_vel_x, player_vel_y, on_ground, platforms,
 coins, enemies, enemy_vel, endpoint, score, game_over, game_win) = reset_game(current_level)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if (game_over or game_win) and event.key == pygame.K_SPACE:
                if game_win:
                    current_level = current_level + 1 if current_level < max_levels else 1
                (player, player_vel_x, player_vel_y, on_ground, platforms,
                 coins, enemies, enemy_vel, endpoint, score, game_over, game_win) = reset_game(current_level)
            if not game_over and not game_win:
                if event.key == pygame.K_LEFT:
                    player_vel_x = -5
                if event.key == pygame.K_RIGHT:
                    player_vel_x = 5
                if event.key == pygame.K_SPACE and on_ground:
                    player_vel_y = jump_power
                    on_ground = False
        if event.type == pygame.KEYUP and not game_over and not game_win:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                player_vel_x = 0

    # Game logic
    if not game_over and not game_win:
        player.x += player_vel_x
        player_vel_y += gravity
        player.y += player_vel_y
        on_ground = False

        for platform in platforms:
            if player.colliderect(platform) and player_vel_y >= 0 and player.bottom <= platform.bottom:
                player.bottom = platform.top
                player_vel_y = 0
                on_ground = True

        if player.left < 0:
            player.left = 0
        if player.right > WIDTH:
            player.right = WIDTH

        for coin in coins[:]:
            if player.colliderect(coin):
                coins.remove(coin)
                score += 1

        for enemy in enemies:
            enemy.x += enemy_vel
            if enemy.left <= 0 or enemy.right >= WIDTH:
                enemy_vel *= -1
            if player.colliderect(enemy):
                game_over = True

        if player.colliderect(endpoint) and len(coins) == 0:
            game_win = True

        if player.top > HEIGHT:
            game_over = True

    # Drawing
    screen.fill(SKYBLUE)
    draw_cloud(150, 80)
    draw_cloud(500, 60)

    for platform in platforms:
        pygame.draw.rect(screen, BLACK, platform)
    for coin in coins:
        pygame.draw.circle(screen, GOLD, coin.center, coin_size // 2)
    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy)
    pygame.draw.rect(screen, BLUE, endpoint)

    # Draw player using image
    screen.blit(player_img, player.topleft)

    # UI text
    level_text = font.render(f"Level: {current_level}", True, BLACK)
    screen.blit(level_text, (WIDTH - 150, 10))
    score_text = font.render(f"Coins Collected: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    if game_over:
        over_text = font.render("Game Over! Press Space to Restart.", True, RED)
        screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2))
    elif game_win:
        if current_level == max_levels:
            win_text = font.render("All Levels Complete! Press Space.", True, BLUE)
        else:
            win_text = font.render("Level Complete! Press Space for Next.", True, BLUE)
        screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2))

    pygame.display.flip()
    clock.tick(FPS)
