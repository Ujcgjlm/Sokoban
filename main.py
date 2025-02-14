import pygame
import sys
import os
import time
from src.load_images import load_images
from src.settings import Settings
from src.level import Level

class Renderer:
    def __init__(self, settings):
        self.settings = settings
        self.images = {}
        self.load_theme_images()

    def load_theme_images(self):
        self.images = load_images(self.settings.current_theme)

    def draw_level(self, level):
        for y, row in enumerate(level.data):
            for x, tile in enumerate(row):
                if sprite := self.images.get(tile):
                    self.settings.screen.blit(
                        sprite, (x * self.settings.TILE_SIZE, y * self.settings.TILE_SIZE))

    def draw_status(self, start_time, move_history):
        elapsed_time = time.time() - start_time
        timer_text = f"Time: {int(elapsed_time)}s"
        steps_text = f"Steps: {len(move_history)}"
        timer_surface = self.settings.font.render(timer_text, True, self.settings.COLORS['BLACK'])
        steps_surface = self.settings.font.render(steps_text, True, self.settings.COLORS['BLACK'])
        self.settings.screen.blit(timer_surface, (self.settings.SCREEN_WIDTH - 200, 20))
        self.settings.screen.blit(steps_surface, (self.settings.SCREEN_WIDTH - 200, 60))

class Menu:
    def __init__(self, settings):
        self.settings = settings
        self.selected_button = 0
        self.scroll_offset = 0
        self.visible_levels = 6

    def draw_main_menu(self):
        self.settings.screen.fill(self.settings.COLORS['MENU_BG'])
        title_surface = self.settings.title_font.render("Sokoban", True, self.settings.COLORS['HIGHLIGHT'])
        title_rect = title_surface.get_rect(center=(self.settings.SCREEN_WIDTH//2, 100))
        self.settings.screen.blit(title_surface, title_rect)

        buttons = ["Уровни", "Выход"]
        for i, text in enumerate(buttons):
            rect = pygame.Rect(0, 0, 300, 60)
            rect.center = (self.settings.SCREEN_WIDTH//2, 250 + i*100)
            color = self.settings.COLORS['HIGHLIGHT'] if i == self.selected_button else self.settings.COLORS['BUTTON_BG']
            pygame.draw.rect(self.settings.screen, color, rect, border_radius=8)
            text_surface = self.settings.font.render(text, True, self.settings.COLORS['WHITE'])
            text_rect = text_surface.get_rect(center=rect.center)
            self.settings.screen.blit(text_surface, text_rect)
        pygame.display.flip()

    def draw_level_menu(self, selected_level, completed_levels, total_levels):
        self.settings.screen.fill(self.settings.COLORS['MENU_BG'])
        title_surface = self.settings.title_font.render("Выберите уровень", True, self.settings.COLORS['HIGHLIGHT'])
        title_rect = title_surface.get_rect(center=(self.settings.SCREEN_WIDTH//2, 50))
        self.settings.screen.blit(title_surface, title_rect)

        list_width = 400
        list_height = 360
        list_x = (self.settings.SCREEN_WIDTH - list_width) // 2
        pygame.draw.rect(self.settings.screen, self.settings.COLORS['BUTTON_BG'],
                        (list_x - 10, 90, list_width + 20, list_height + 20),
                        border_radius=12)

        for i in range(self.scroll_offset, min(self.scroll_offset + self.visible_levels, total_levels)):
            idx = i - self.scroll_offset
            btn_rect = pygame.Rect(list_x, 100 + idx * 60, list_width, 50)
            color = self.settings.COLORS['HIGHLIGHT'] if i == selected_level else self.settings.COLORS['GRAY']
            pygame.draw.rect(self.settings.screen, color, btn_rect, border_radius=8)

            level_text = f"Level {i + 1}"
            text_surface = self.settings.font.render(level_text, True, self.settings.COLORS['WHITE'])
            text_rect = text_surface.get_rect(center=btn_rect.center)
            self.settings.screen.blit(text_surface, text_rect)

            if i in completed_levels:
                check_rect = pygame.Rect(btn_rect.right - 45, btn_rect.centery - 15, 30, 30)
                pygame.draw.circle(self.settings.screen, (0, 200, 0), check_rect.center, 12)

        if total_levels > self.visible_levels:
            scroll_height = list_height * (self.visible_levels / total_levels)
            scroll_y = 100 + (self.scroll_offset / total_levels) * list_height
            pygame.draw.rect(self.settings.screen, self.settings.COLORS['HIGHLIGHT'],
                           (list_x + list_width + 5, scroll_y, 8, scroll_height),
                           border_radius=4)

        controls_text = "↑/↓: Навигация | ENTER: Выбор | ESC: Назад"
        controls_surface = self.settings.font.render(controls_text, True, self.settings.COLORS['WHITE'])
        self.settings.screen.blit(controls_surface, (50, self.settings.SCREEN_HEIGHT - 60))
        pygame.display.flip()

class Game:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.renderer = Renderer(self.settings)
        self.menu = Menu(self.settings)
        self.clock = pygame.time.Clock()
        self.levels = self.load_levels()
        self.completed_levels = self.load_progress()

    def load_levels(self):
        if not os.path.exists(self.settings.LEVELS_DIR):
            print(f"Error: Directory '{self.settings.LEVELS_DIR}' not found.")
            return []

        levels = []
        for filename in sorted(os.listdir(self.settings.LEVELS_DIR)):
            if not filename.endswith('.txt'):
                continue
            with open(os.path.join(self.settings.LEVELS_DIR, filename), 'r') as file:
                # Читаем все строки и удаляем пробелы справа
                lines = [line.rstrip() for line in file.readlines()]
                # Удаляем пустые строки в начале и конце
                while lines and not lines[0].strip():
                    lines.pop(0)
                while lines and not lines[-1].strip():
                    lines.pop()
                
                if not lines:
                    continue

                # Находим максимальную длину строки
                max_width = max(len(line) for line in lines)
                # Дополняем все строки пробелами до максимальной длины
                level = [line.ljust(max_width) for line in lines]
                levels.append(level)
        return levels

    def load_progress(self):
        if not os.path.exists(self.settings.SAVE_FILE):
            return set()
        with open(self.settings.SAVE_FILE, "r") as f:
            return set(int(line.strip()) for line in f.readlines())

    def save_progress(self):
        with open(self.settings.SAVE_FILE, "w") as f:
            for level in self.completed_levels:
                f.write(f"{level}\n")

    def handle_main_menu(self):
        while True:
            self.menu.draw_main_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.menu.selected_button = max(0, self.menu.selected_button - 1)
                    elif event.key == pygame.K_DOWN:
                        self.menu.selected_button = min(1, self.menu.selected_button + 1)
                    elif event.key == pygame.K_RETURN:
                        if self.menu.selected_button == 0:
                            return True
                        elif self.menu.selected_button == 1:
                            return False
        return True

    def handle_level_selection(self):
        selected_level = 0
        while True:
            self.menu.draw_level_menu(selected_level, self.completed_levels, len(self.levels))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return -1
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and selected_level > 0:
                        selected_level -= 1
                        if selected_level < self.menu.scroll_offset:
                            self.menu.scroll_offset = max(0, self.menu.scroll_offset - 1)
                    elif event.key == pygame.K_DOWN and selected_level < len(self.levels) - 1:
                        selected_level += 1
                        if selected_level >= self.menu.scroll_offset + self.menu.visible_levels:
                            self.menu.scroll_offset = min(
                                len(self.levels) - self.menu.visible_levels,
                                self.menu.scroll_offset + 1
                            )
                    elif event.key == pygame.K_RETURN:
                        return selected_level
                    elif event.key == pygame.K_ESCAPE:
                        return -1
        return -1

    def play_level(self, level_index):
        level = Level(self.levels[level_index])
        move_history = []
        start_time = time.time()
        move_key_delay = 100
        last_move_time = 0
        undo_key_delay = 80
        last_undo_time = 0

        print(f"\nНачинаем уровень {level_index + 1}")

        while True:
            current_time = pygame.time.get_ticks()
            keys = pygame.key.get_pressed()
            dx, dy = 0, 0

            if keys[pygame.K_LEFT]: dx = -1
            elif keys[pygame.K_RIGHT]: dx = 1
            elif keys[pygame.K_UP]: dy = -1
            elif keys[pygame.K_DOWN]: dy = 1

            if (dx != 0 or dy != 0) and (current_time - last_move_time > move_key_delay):
                move_history.append([row[:] for row in level.data])
                if level.move_player(dx, dy):
                    last_move_time = current_time
                else:
                    move_history.pop()

            if keys[pygame.K_u] and move_history and (current_time - last_undo_time > undo_key_delay):
                last_undo_time = current_time
                if move_history:
                    print("\nОтмена хода")
                    level.data = move_history.pop()
                    level.find_player()
                    level.moves_count -= 1
                    # level.print_board()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        print("\nПерезапуск уровня")
                        level = Level(self.levels[level_index])
                        move_history.clear()
                        start_time = time.time()
                    elif event.key == pygame.K_t:
                        theme = "dark" if self.settings.current_theme == "default" else "default"
                        print(f"\nСмена темы на: {theme}")
                        self.settings.current_theme = theme
                        self.renderer.load_theme_images()
                    elif event.key in (pygame.K_m, pygame.K_ESCAPE):
                        print("\nВыход в меню")
                        return True

            if level.check_win():
                elapsed_time = int(time.time() - start_time)
                print(f"\nУровень {level_index + 1} пройден!")
                print(f"Время прохождения: {elapsed_time} секунд")
                print(f"Количество ходов: {level.moves_count}")
                self.completed_levels.add(level_index)
                self.save_progress()
                return True

            self.settings.screen.fill(self.settings.get_backcolor())
            self.renderer.draw_level(level)
            self.renderer.draw_status(start_time, move_history)
            pygame.display.flip()
            self.clock.tick(60)

    def run(self):
        if not self.levels:
            print("No levels to load. Please check the 'levels' directory.")
            return

        while True:
            if not self.handle_main_menu():
                break

            level_index = self.handle_level_selection()
            if level_index == -1:
                continue

            if not self.play_level(level_index):
                break

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    os.makedirs(Settings().LEVELS_DIR, exist_ok=True)
    game = Game()
    game.run()
