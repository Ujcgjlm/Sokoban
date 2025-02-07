import pygame
import sys
import os
import time

from src.load_images import load_images
from src.settings import Settings

pygame.init()

def load_levels(settings):
    if not os.path.exists(settings.LEVELS_DIR):
        print(f"Error: Directory '{settings.LEVELS_DIR}' not found.")
        return []

    levels = []
    for filename in sorted(os.listdir(settings.LEVELS_DIR)):
        with open(os.path.join(settings.LEVELS_DIR, filename), 'r') as file:
            lines = file.readlines()
            level = [line for line in lines]
            levels.append(level)
    return levels

def save_progress(settings, completed_levels):
    with open(settings.SAVE_FILE, "w") as f:
        for level in completed_levels:
            f.write(f"{level}\n")

def load_progress(settings):
    if not os.path.exists(settings.SAVE_FILE):
        return set()
    
    with open(settings.SAVE_FILE, "r") as f:
        return set(int(line.strip()) for line in f.readlines())

def find_goals(level):
    goals = []
    for y, row in enumerate(level):
        for x, tile in enumerate(row):
            if tile == '.':
                goals.append((x, y))
    return goals

def draw_level(settings, level, goals):
    images = load_images(settings.current_theme)
    for y, row in enumerate(level):
        for x, tile in enumerate(row):
            if (x, y) in goals:
                settings.screen.blit(images['.'], (x * settings.TILE_SIZE, y * settings.TILE_SIZE))
            if sprite := images.get(tile, None):
                settings.screen.blit(sprite, (x * settings.TILE_SIZE, y * settings.TILE_SIZE))

def move_player(settings, level, goals, dx, dy):
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
        elif level[ny][nx] in {'$', '*'}:
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
    return not any('$' in row for row in level)

def draw_status(settings, start_time, steps):
    elapsed_time = time.time() - start_time
    timer_text = f"Time: {int(elapsed_time)}s"
    steps_text = f"Steps: {steps}"
    timer_surface = settings.font.render(timer_text, True, settings.COLORS['BLACK'])
    steps_surface = settings.font.render(steps_text, True, settings.COLORS['BLACK'])
    
    settings.screen.blit(timer_surface, (settings.SCREEN_WIDTH - 200, 20))
    settings.screen.blit(steps_surface, (settings.SCREEN_WIDTH - 200, 60))

def draw_main_menu(settings, selected_button):
    settings.screen.fill(settings.COLORS['MENU_BG'])

    title_surface = settings.title_font.render("Sokoban", True, settings.COLORS['HIGHLIGHT'])
    title_rect = title_surface.get_rect(center=(settings.SCREEN_WIDTH//2, 100))
    settings.screen.blit(title_surface, title_rect)

    buttons = ["Уровни", "Выход"]

    for i, text in enumerate(buttons):
        rect = pygame.Rect(0, 0, 300, 60)
        rect.center = (settings.SCREEN_WIDTH//2, 250 + i*100)
        color = settings.COLORS['HIGHLIGHT'] if i == selected_button else settings.COLORS['BUTTON_BG']
        
        pygame.draw.rect(settings.screen, color, rect, border_radius=8)
        text_surface = settings.font.render(text, True, settings.COLORS['WHITE'])
        text_rect = text_surface.get_rect(center=rect.center)
        settings.screen.blit(text_surface, text_rect)

    pygame.display.flip()

def main_menu(settings):
    selected_button = 0
    while True:
        draw_main_menu(settings, selected_button)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_button = max(0, selected_button - 1)
                elif event.key == pygame.K_DOWN:
                    selected_button = min(1, selected_button + 1)
                elif event.key == pygame.K_RETURN:
                    if selected_button == 0:
                        return
                    elif selected_button == 1:
                        pygame.quit()
                        sys.exit()

def level_selector(settings, levels):
    total_levels = len(levels)
    scroll_offset = 0
    visible_levels = 6
    selected_level = 0
    completed_levels = load_progress(settings)

    while True:
        draw_level_menu(settings, selected_level, completed_levels, total_levels, scroll_offset)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if selected_level > 0:
                        selected_level -= 1
                        if selected_level < scroll_offset:
                            scroll_offset = max(0, scroll_offset - 1)
                elif event.key == pygame.K_DOWN:
                    if selected_level < total_levels - 1:
                        selected_level += 1
                        if selected_level >= scroll_offset + visible_levels:
                            scroll_offset = min(total_levels - visible_levels, scroll_offset + 1)
                elif event.key == pygame.K_RETURN:
                    return selected_level, completed_levels
                elif event.key == pygame.K_ESCAPE:
                    return -1, completed_levels

def draw_level_menu(settings, selected_level, completed_levels, total_levels, scroll_offset):
    settings.screen.fill(settings.COLORS['MENU_BG'])

    title_surface = settings.title_font.render("Выберите уровень", True, settings.COLORS['HIGHLIGHT'])
    title_rect = title_surface.get_rect(center=(settings.SCREEN_WIDTH//2, 50))
    settings.screen.blit(title_surface, title_rect)

    list_width = 400
    list_height = 360
    list_x = (settings.SCREEN_WIDTH - list_width) // 2
    pygame.draw.rect(settings.screen, settings.COLORS['BUTTON_BG'], 
                    (list_x - 10, 90, list_width + 20, list_height + 20), 
                    border_radius=12)

    visible_levels = min(6, total_levels)
    for i in range(scroll_offset, min(scroll_offset + visible_levels, total_levels)):
        idx = i - scroll_offset
        btn_rect = pygame.Rect(list_x, 100 + idx * 60, list_width, 50)
        
        if i == selected_level:
            pygame.draw.rect(settings.screen, settings.COLORS['HIGHLIGHT'], btn_rect, border_radius=8)
        else:
            pygame.draw.rect(settings.screen, settings.COLORS['GRAY'], btn_rect, border_radius=8)

        level_text = f"Level {i + 1}"
        text_surface = settings.font.render(level_text, True, settings.COLORS['WHITE'])
        text_rect = text_surface.get_rect(center=btn_rect.center)
        settings.screen.blit(text_surface, text_rect)

        if i in completed_levels:
            check_rect = pygame.Rect(btn_rect.right - 45, btn_rect.centery - 15, 30, 30)
            pygame.draw.circle(settings.screen, (0, 200, 0), check_rect.center, 12)

    if total_levels > visible_levels:
        scroll_height = list_height * (visible_levels / total_levels)
        scroll_y = 100 + (scroll_offset / total_levels) * list_height
        pygame.draw.rect(settings.screen, settings.COLORS['HIGHLIGHT'],
                        (list_x + list_width + 5, scroll_y, 8, scroll_height),
                        border_radius=4)

    controls_text = "↑/↓: Навигация | ENTER: Выбор | ESC: Назад"
    controls_surface = settings.font.render(controls_text, True, settings.COLORS['WHITE'])
    settings.screen.blit(controls_surface, (50, settings.SCREEN_HEIGHT - 60))

    pygame.display.flip()

def main():
    settings = Settings()
    levels = load_levels(settings)
    
    if not levels:
        print("No levels to load. Please check the 'levels' directory.")
        return

    while True:
        main_menu(settings)
        
        current_level_index, completed_levels = level_selector(settings, levels)
        if current_level_index == -1:
            continue

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
                        dx, dy = 0, 0
                        if event.key == pygame.K_LEFT: dx = -1
                        if event.key == pygame.K_RIGHT: dx = 1
                        if event.key == pygame.K_UP: dy = -1
                        if event.key == pygame.K_DOWN: dy = 1
                        
                        level, moved = move_player(settings, level, goals, dx, dy)
                        if moved: steps += 1

                    if event.key == pygame.K_u and move_history:
                        level = move_history.pop()
                        if steps > 0: steps -= 1

                    if event.key == pygame.K_r:
                        level = [row[:] for row in original_level]
                        move_history.clear()
                        steps = 0
                        start_time = time.time()

                    if event.key == pygame.K_t:
                        settings.current_theme = "dark" if settings.current_theme == "default" else "default"

                    if event.key in (pygame.K_m, pygame.K_ESCAPE):
                        break

            else:
                if check_win(level):
                    print("Уровень пройден!")
                    completed_levels.add(current_level_index)
                    save_progress(settings, completed_levels)
                    break

                settings.screen.fill(settings.get_backcolor())
                draw_level(settings, level, goals)
                draw_status(settings, start_time, steps)
                pygame.display.flip()
                clock.tick(60)
                continue

            break

if __name__ == "__main__":
    os.makedirs(Settings().LEVELS_DIR, exist_ok=True)
    main()
