import pygame

class GeneratorSettings:
    def __init__(self, settings):
        self.settings = settings
        self.width = 7
        self.height = 7
        self.wall_chance = 0.3
        self.box_chance = 0.25
        self.target_chance = 0.2
        self.sliders = []
        self.active_slider = None
        self.init_sliders()
        self.generation_progress = 0
        self.is_generating = False
        self.solver_progress = 0

    def init_sliders(self):
        slider_width = 250
        slider_height = 15
        slider_spacing = 60
        start_x = (self.settings.SCREEN_WIDTH - slider_width) // 2
        start_y = 250

        self.sliders = [
            {
                'name': 'Ширина',
                'value': self.width,
                'min': 5,
                'max': 15,
                'rect': pygame.Rect(start_x, start_y, slider_width, slider_height)
            },
            {
                'name': 'Высота',
                'value': self.height,
                'min': 5,
                'max': 15,
                'rect': pygame.Rect(start_x, start_y + slider_spacing, slider_width, slider_height)
            },
            {
                'name': 'Шанс стен',
                'value': self.wall_chance,
                'min': 0,
                'max': 0.5,
                'rect': pygame.Rect(start_x, start_y + slider_spacing * 2, slider_width, slider_height)
            },
            {
                'name': 'Шанс ящиков',
                'value': self.box_chance,
                'min': 0.1,
                'max': 0.9,
                'rect': pygame.Rect(start_x, start_y + slider_spacing * 3, slider_width, slider_height)
            },
            {
                'name': 'Шанс целей',
                'value': self.target_chance,
                'min': 0.1,
                'max': 0.4,
                'rect': pygame.Rect(start_x, start_y + slider_spacing * 4, slider_width, slider_height)
            }
        ]

    def draw(self, screen):
        for slider in self.sliders:
            pygame.draw.rect(screen, self.settings.COLORS['GRAY'], slider['rect'], border_radius=8)

            handle_x = slider['rect'].x + (slider['rect'].width - 15) * ((slider['value'] - slider['min']) / (slider['max'] - slider['min']))
            handle_rect = pygame.Rect(handle_x, slider['rect'].y - 3, 15, 21)
            pygame.draw.rect(screen, self.settings.COLORS['HIGHLIGHT'], handle_rect, border_radius=8)

            value = int(slider['value']) if slider['name'] in ['Ширина', 'Высота'] else f"{slider['value']:.2f}"
            text = f"{slider['name']}: {value}"
            text_surface = self.settings.font.render(text, True, self.settings.COLORS['WHITE'])
            text_rect = text_surface.get_rect(center=(slider['rect'].centerx, slider['rect'].y - 20))
            screen.blit(text_surface, text_rect)

        if self.is_generating:
            progress_width = 400
            progress_height = 25
            progress_x = (self.settings.SCREEN_WIDTH - progress_width) // 2
            progress_y = 550

            pygame.draw.rect(screen, self.settings.COLORS['GRAY'], 
                           (progress_x, progress_y, progress_width, progress_height), 
                           border_radius=12)

            fill_width = int(progress_width * self.solver_progress)
            if fill_width > 0:
                pygame.draw.rect(screen, self.settings.COLORS['HIGHLIGHT'],
                               (progress_x, progress_y, fill_width, progress_height),
                               border_radius=12)

            progress_text = f"Проверка уровня... {int(self.solver_progress * 100)}%"
            text_surface = self.settings.font.render(progress_text, True, self.settings.COLORS['WHITE'])
            text_rect = text_surface.get_rect(center=(self.settings.SCREEN_WIDTH//2, progress_y - 30))
            screen.blit(text_surface, text_rect)

    def handle_mouse_down(self, pos):
        for slider in self.sliders:
            handle_x = slider['rect'].x + (slider['rect'].width - 15) * ((slider['value'] - slider['min']) / (slider['max'] - slider['min']))
            handle_rect = pygame.Rect(handle_x, slider['rect'].y - 3, 15, 21)
            if handle_rect.collidepoint(pos):
                self.active_slider = slider
                self.update_slider_value(pos[0])
                break

    def handle_mouse_up(self):
        self.active_slider = None

    def handle_mouse_motion(self, pos):
        if self.active_slider:
            self.update_slider_value(pos[0])

    def update_slider_value(self, x):
        if not self.active_slider:
            return

        slider = self.active_slider
        relative_x = max(0, min(1, (x - slider['rect'].x) / slider['rect'].width))
        slider['value'] = slider['min'] + (slider['max'] - slider['min']) * relative_x

        if slider['name'] == 'Ширина':
            self.width = int(slider['value'])
        elif slider['name'] == 'Высота':
            self.height = int(slider['value'])
        elif slider['name'] == 'Шанс стен':
            self.wall_chance = slider['value']
        elif slider['name'] == 'Шанс ящиков':
            self.box_chance = slider['value']
        elif slider['name'] == 'Шанс целей':
            self.target_chance = slider['value']

    def get_settings(self):
        return {
            'width': self.width,
            'height': self.height,
            'wall_chance': self.wall_chance,
            'box_chance': self.box_chance,
            'target_chance': self.target_chance
        }

    def update_solver_progress(self, progress):
        self.solver_progress = progress

    def start_generation(self):
        self.is_generating = True
        self.solver_progress = 0

    def finish_generation(self):
        self.is_generating = False
        self.solver_progress = 0 