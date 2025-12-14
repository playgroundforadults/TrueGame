import pygame
from settings import *

class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(ui_font, ui_font_size)

        self.health_bar_rect = pygame.Rect(10, 10, health_bar_width, bar_height)
        self.magic_bar_rect = pygame.Rect(10, 34, magic_bar_width, bar_height)


    def show_bar(self, current, max_amount, bg_rect, color):
        self.display_surface.fill(ui_bg_color, bg_rect)
        # calculate ratio
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width
        self.display_surface.fill(color, current_rect)
        pygame.draw.rect(self.display_surface, color, current_rect)

        pygame.draw.rect(self.display_surface, ui_border_color, bg_rect, 3)

    def show_exp(self, exp):
        text_surf = self.font.render(f'Exp: {exp}', False, text_color)
        text_rect = text_surf.get_rect(topleft=(10, 60))

        self.display_surface.blit(text_surf, text_rect)

    def display(self, player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, health_color)
        self.show_bar(player.energy, player.stats['energy'], self.magic_bar_rect, energy_color)

        self.show_exp(player.exp)