import pygame
import os

class Settings:
    def __init__(self):
        self.SCREEN_WIDTH = 1000
        self.SCREEN_HEIGHT = 600
        self.TILE_SIZE = 36
        self.COLORS = {
            'BLACK': (0, 0, 0),
            'WHITE': (255, 255, 255),
            'GRAY': (42, 42, 42),
            'SAND': (220, 212, 171),
            'HIGHLIGHT': (255, 215, 0),
            'MENU_BG': (30, 30, 30),
            'BUTTON_BG': (60, 60, 60)
        }
        self.current_theme = "default"
        self.LEVELS_DIR = "levels"
        self.SAVE_FILE = "progress.dat"
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        font_path = os.path.join("fonts", "arial.ttf")
        bold_font_path = os.path.join("fonts", "arialbd.ttf")
        try:
            self.font = pygame.font.Font(font_path, 32)
            self.title_font = pygame.font.Font(bold_font_path, 48)
        except FileNotFoundError:
            print("Font files not found, using system fonts")
            self.font = pygame.font.SysFont("Arial", 32)
            self.title_font = pygame.font.SysFont("Arial", 48, bold=True)
    
    def get_backcolor(self):
        return self.COLORS['GRAY'] if self.current_theme == "dark" else self.COLORS['SAND']
