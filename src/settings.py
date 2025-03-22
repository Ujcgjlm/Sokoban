import pygame
import os

class Settings:
    def __init__(self):
        self.SCREEN_WIDTH = 1200
        self.SCREEN_HEIGHT = 800
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

        pygame.font.init()
        
        self.font = pygame.font.SysFont("Arial", 32)
        self.title_font = pygame.font.SysFont("Arial", 48, bold=True)
    
    def get_backcolor(self):
        return self.COLORS['GRAY'] if self.current_theme == "dark" else self.COLORS['SAND']
