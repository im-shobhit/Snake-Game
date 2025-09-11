import pygame
import random
import os

pygame.init()

# Colors
WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
RED    = (213, 50, 80)
GREEN  = (0, 255, 0)
YELLOW = (255, 255, 102)

# Initial window size
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Classic Snake - Border & Timer")

clock = pygame.time.Clock()

# Fonts (classic)
font_small = pygame.font.SysFont("couriernew", 20, bold=True)
font_big   = pygame.font.SysFont("couriernew", 36, bold=True)

# Game constants
BLOCK = 20  # also used as border thickness

# High score file
HS_FILE = "highscore.txt"
def load_high_score():
    try:
        if os.path.exists(HS_FILE):
            with open(HS_FILE, "r") as f:
                return int(f.read().strip())
    except:
        pass
    return 0

def save_high_score(score):
    try:
        with open(HS_FILE, "w") as f:
            f.write(str(int(score)))
    except:
        pass

# Playable rectangle helpers (inside the border)
def get_playable_rect():
    w, h = win.get_size()
    t = BLOCK
    return (t, t, w - 2*t, h - 2*t)  # x0, y0, width_inner, height_inner

# Draw solid border (four filled rectangles)
def draw_border_frame():
    w, h = win.get_size()
    t = BLOCK
    # Fill background
    win.fill(BLACK)
    # Top
    pygame.draw.rect(win, WHITE, (0, 0, w, t))
    # Bottom
    pygame.draw.rect(win, WHITE, (0, h - t, w, t))
    # Left
    pygame.draw.rect(win, WHITE, (0, 0, t, h))
    # Right
    pygame.draw.rect(win, WHITE, (w - t, 0, t, h))
    # Fill inside playable area with black (ensures inner stays black)
    win.fill(BLACK, (t, t, w - 2*t, h - 2*t))

# Spawn food snapped to the grid inside playable area
def spawn_food(snake):
    x0, y0, w_inner, h_inner = get_playable_rect()
    cols = max(1, w_inner // BLOCK)
    rows = max(1, h_inner // BLOCK)
    while True:
        fx = x0 + random.randint(0, cols - 1) * BLOCK
        fy = y0 + random.randint(0, rows - 1) * BLOCK
        if (fx, fy) not in snake:
            return fx, fy

# Draw snake blocks
def draw_snake(snake):
    for (sx, sy) in snake:
        pygame.draw.rect(win, GREEN, (sx, sy, BLOCK, BLOCK))

# Centered text helper (y is pixel-coordinate)
def draw_centered(text, y, color=WHITE, font=font_small):
    surf = font.render(text, True, color)
    w, h = win.get_size()
    rect = surf.get_rect(center=(w//2, y))
    win.blit(surf, rect)

# Fullscreen toggle
def toggle_fullscreen():
    global win, WIDTH, HEIGHT
    flags = win.get_flags()
    if flags & pygame.FULLSCREEN:
        win = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        WIDTH, HEIGHT = 800, 600
    else:
        info = pygame.display.Info()
        WIDTH, HEIGHT = info.current_w, info.current_h
        win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

# Start menu — NO border here; menu text centered and responsive
def start_menu():
    while True:
        win.fill(BLACK)  # clear full window (no border at menu)
        w, h = win.get_size()
        draw_centered("=== CLASSIC SNAKE ===", h//3, YELLOW, font_big)
        draw_centered("Select Difficulty (1-Easy, 2-Medium, 3-Hard)", h//2 - 10, WHITE, font_small)
        draw_centered("Press F to toggle Fullscreen | P to Pause during play", h//2 + 40, YELLOW, font_small)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 10
                if event.key == pygame.K_2:
                    return 15
                if event.key == pygame.K_3:
                    return 22
                if event.key == pygame.K_f:
                    toggle_fullscreen()

# Format elapsed milliseconds to mm:ss
def format_time(ms):
    total_secs = max(0, ms // 1000)
    m = total_secs // 60
    s = total_secs % 60
    return f"{m:02d}:{s:02d}"

# MAIN GAME LOOP
def game_loop(base_speed):
    high_score = load_high_score()

    # compute initial spawn position snapped to grid inside playable area
    x0, y0, w_inner, h_inner = get_playable_rect()
    cols = max(1, w_inner // BLOCK)
    rows = max(1, h_inner // BLOCK)
    x = x0 + (cols // 2) * BLOCK
    y = y0 + (rows // 2) * BLOCK

    dx = 0
    dy = 0
    snake = [(x, y)]
    length = 1
    foodx, foody = spawn_food(snake)
    score = 0
    speed = float(base_speed)

    # Timer handling
    start_ticks = pygame.time.get_ticks()
    paused = False
    pause_start = 0
    paused_total = 0

    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_high_score(high_score)
                pygame.quit()
                return
            if event.type == pygame.VIDEORESIZE:
                # update display surface in windowed resize
                global WIDTH, HEIGHT, win
                WIDTH, HEIGHT = event.w, event.h
                win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and dx == 0:
                    dx, dy = -BLOCK, 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx, dy = BLOCK, 0
                elif event.key == pygame.K_UP and dy == 0:
                    dx, dy = 0, -BLOCK
                elif event.key == pygame.K_DOWN and dy == 0:
                    dx, dy = 0, BLOCK
                elif event.key == pygame.K_p:
                    # toggle pause and manage pause timer
                    if not paused:
                        paused = True
                        pause_start = pygame.time.get_ticks()
                    else:
                        paused = False
                        paused_total += pygame.time.get_ticks() - pause_start
                elif event.key == pygame.K_f:
                    toggle_fullscreen()
                elif event.key == pygame.K_c and game_over:
                    return game_loop(base_speed)  # restart preserving difficulty
                elif event.key == pygame.K_q and game_over:
                    save_high_score(high_score)
                    pygame.quit()
                    return

        if paused:
            # draw border and paused message inside playable area
            draw_border_frame()
            draw_centered("PAUSED - Press P to Resume", win.get_size()[1] // 2, YELLOW, font_big)
            pygame.display.update()
            clock.tick(10)
            continue

        if not game_over:
            # move
            x += dx
            y += dy

            # update playable rect each frame (in case of resize/fullscreen)
            x0, y0, w_inner, h_inner = get_playable_rect()

            # Check collisions with border (game over if snake enters border area)
            if (x < x0) or (x >= x0 + w_inner) or (y < y0) or (y >= y0 + h_inner):
                game_over = True

            # update snake body
            snake.append((x, y))
            if len(snake) > length:
                snake.pop(0)

            # self collision
            if (dx != 0 or dy != 0) and (x, y) in snake[:-1]:
                game_over = True

            # eating food
            if (x, y) == (foodx, foody):
                length += 1
                score += 10
                if score > high_score:
                    high_score = score
                    save_high_score(high_score)
                foodx, foody = spawn_food(snake)
                speed = min(speed + 0.6, 60)

        # DRAW
        draw_border_frame()

        # draw food and snake inside playable area
        pygame.draw.rect(win, RED, (foodx, foody, BLOCK, BLOCK))
        draw_snake(snake)

        # compute dynamic positions for score & timer inside playable rect (won't overlap border)
        x0, y0, w_inner, h_inner = get_playable_rect()
        padding = 6
        # Score top-left inside playable area
        score_surf = font_small.render(f"Score: {score}", True, YELLOW)
        win.blit(score_surf, (x0 + padding, y0 + padding))
        # Highscore top-right inside playable area
        hs_surf = font_small.render(f"High: {high_score}", True, YELLOW)
        win.blit(hs_surf, (x0 + w_inner - hs_surf.get_width() - padding, y0 + padding))
        # Timer centered at top inside playable area
        if not paused and not game_over:
            elapsed = pygame.time.get_ticks() - start_ticks - paused_total
        else:
            # when paused or game_over, don't advance; show current elapsed
            elapsed = (pause_start - start_ticks - paused_total) if paused and pause_start else (pygame.time.get_ticks() - start_ticks - paused_total if not game_over else pygame.time.get_ticks() - start_ticks - paused_total)
        time_surf = font_small.render(f"Time: {format_time(elapsed)}", True, YELLOW)
        win.blit(time_surf, (x0 + (w_inner - time_surf.get_width()) // 2, y0 + padding))

        # game over overlay text (centered)
        if game_over:
            draw_centered("=== GAME OVER ===", win.get_size()[1] // 3, RED, font_big)
            draw_centered("Press C to Restart or Q to Quit", win.get_size()[1] // 2, WHITE, font_small)

        pygame.display.update()
        clock.tick(int(speed if speed > 1 else 1))

# Run
if __name__ == "__main__":
    difficulty = start_menu()
    if difficulty:
        game_loop(difficulty)
