import pygame
import sys
import os
import time

from src.load_images import load_images

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600
TILE_SIZE = 36
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (42, 42, 42)
SAND = (220, 212, 171)

current_theme = "default"
def get_backcolor(theme):
    return GRAY if theme == "dark" else SAND

LEVELS_DIR = "levels"
SAVE_FILE = "progress.dat"

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sokoban")

font = pygame.font.Font(None, 36)

def load_levels(directory):
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' not found.")
        return []

    levels = []
    for filename in sorted(os.listdir(directory)):
        with open(os.path.join(directory, filename), 'r') as file:
            lines = file.readlines()
            level = [line for line in lines]
            levels.append(level)
    return levels

def save_progress(completed_levels):
    with open(SAVE_FILE, "w") as f:
        for level in completed_levels:
            f.write(f"{level}\n")

def load_progress():
    if not os.path.exists(SAVE_FILE):
        return set()
    
    with open(SAVE_FILE, "r") as f:
        return set(int(line.strip()) for line in f.readlines())

def find_goals(level):
    goals = []
    for y, row in enumerate(level):
        for x, tile in enumerate(row):
            if tile == '.':
                goals.append((x, y))
    return goals

def draw_level(level, goals):
    images = load_images(current_theme)
    for y, row in enumerate(level):
        for x, tile in enumerate(row):
            if (x, y) in goals:
                screen.blit(images['.'], (x * TILE_SIZE, y * TILE_SIZE))
            if sprite := images.get(tile, None):
                screen.blit(sprite, (x * TILE_SIZE, y * TILE_SIZE))

def move_player(level, goals, dx, dy):
    new_level = [list(row) for row in level]
    player_pos = None
    
    for y, row in enumerate(level):
        for x, char in enumerate(row):
            if char == '@':
                player_pos = (x, y)
                break
        if player_pos:
            break
    
    moved = False
    if player_pos:
        px, py = player_pos
        nx, ny = px + dx, py + dy
        if level[ny][nx] in " .":
            new_level[py][px], new_level[ny][nx] = (' ', '@') if level[py][px] == '@' else ('.', '@')
            moved = True
        elif level[ny][nx] == '$' or level[ny][nx] == '*':
            nnx, nny = nx + dx, ny + dy
            if level[nny][nnx] in " .":
                new_level[py][px] = ' ' if level[py][px] == '@' else '.'
                new_level[ny][nx] = '@'
                new_level[nny][nnx] = '*' if level[nny][nnx] == '.' else '$'
                moved = True
    
    for (gx, gy) in goals:
        if new_level[gy][gx] == ' ':
            new_level[gy][gx] = '.'

    return [''.join(row) for row in new_level], moved

def check_win(level):
    for row in level:
        if '$' in row:
            return False
    return True

def draw_status(start_time, steps):
    elapsed_time = time.time() - start_time
    timer_text = f"Time: {int(elapsed_time)}s"
    steps_text = f"Steps: {steps}"
    timer_surface = font.render(timer_text, True, BLACK)
    steps_surface = font.render(steps_text, True, BLACK)
    
    screen.blit(timer_surface, (SCREEN_WIDTH - 200, 20))
    screen.blit(steps_surface, (SCREEN_WIDTH - 200, 60))

def draw_level_menu(selected_level, completed_levels, total_levels):
    screen.fill(get_backcolor(current_theme))
    title_surface = font.render("Select a Level", True, BLACK)
    screen.blit(title_surface, ((SCREEN_WIDTH - title_surface.get_width()) // 2, 50))
    
    for i in range(total_levels):
        level_text = f"Level {i + 1} {'(Completed)' if i in completed_levels else ''}"
        color = BLACK if i == selected_level else GRAY
        level_surface = font.render(level_text, True, color)
        screen.blit(level_surface, (SCREEN_WIDTH // 2 - 100, 150 + i * 40))
    
    pygame.display.flip()

def level_selector(levels):
    total_levels = len(levels)
    selected_level = 0
    completed_levels = load_progress()

    while True:
        draw_level_menu(selected_level, completed_levels, total_levels)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_level = (selected_level - 1) % total_levels
                if event.key == pygame.K_DOWN:
                    selected_level = (selected_level + 1) % total_levels
                if event.key == pygame.K_RETURN:
                    return selected_level, completed_levels

def main():
    global current_theme

    levels = load_levels(LEVELS_DIR)
    if not levels:
        print("No levels to load. Please check the 'levels' directory.")
        return

    while True:
        current_level_index, completed_levels = level_selector(levels)
        original_level = levels[current_level_index]
        level = [row[:] for row in original_level]
        goals = find_goals(level)

        move_history = []
        steps = 0

        clock = pygame.time.Clock()
        start_time = time.time()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                        move_history.append([row[:] for row in level])
                        if event.key == pygame.K_LEFT:
                            level, moved = move_player(level, goals, -1, 0)
                        if event.key == pygame.K_RIGHT:
                            level, moved = move_player(level, goals, 1, 0)
                        if event.key == pygame.K_UP:
                            level, moved = move_player(level, goals, 0, -1)
                        if event.key == pygame.K_DOWN:
                            level, moved = move_player(level, goals, 0, 1)
                        
                        if moved:
                            steps += 1

                    if event.key == pygame.K_u and move_history:
                        level = move_history.pop()
                        if steps > 0:
                            steps -= 1

                    if event.key == pygame.K_r:
                        level = [row[:] for row in original_level]
                        move_history.clear()
                        steps = 0
                        start_time = time.time()

                    if event.key == pygame.K_t:
                        current_theme = "dark" if current_theme == "default" else "default"

                    if event.key == pygame.K_m or event.key == pygame.K_ESCAPE:
                        break

            else:
                if check_win(level):
                    print("Уровень пройден!")
                    completed_levels.add(current_level_index)
                    save_progress(completed_levels)
                    break

                screen.fill(get_backcolor(current_theme))
                draw_level(level, goals)
                draw_status(start_time, steps)
                pygame.display.flip()
                clock.tick(60)
                continue

            break

if __name__ == "__main__":
    os.makedirs(LEVELS_DIR, exist_ok=True)
    main()
