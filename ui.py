import pygame
from settings import *

class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(ui_font, ui_font_size)

        self.health_bar_rect = pygame.Rect(10, 10, health_bar_width, bar_height)
        self.magic_bar_rect = pygame.Rect(10, 34, magic_bar_width, bar_height)

        self.weapon_graphics = []
        for weapon in weapons_data.values():
            path = weapon['graphic']
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)
        
        self.magic_graphics = []
        for magic in magic_data.values():
            path = magic['graphic']
            magic_surf = pygame.image.load(path).convert_alpha()
            self.magic_graphics.append(magic_surf)


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

    def selection_box(self, left, top, active=False):
        bg_rect = pygame.Rect(left, top, item_box_size, item_box_size)
        pygame.draw.rect(self.display_surface, ui_bg_color, bg_rect)
        border_color = ui_border_color_active if active else ui_border_color
        pygame.draw.rect(self.display_surface, border_color, bg_rect, 3)
        return bg_rect

    def weapon_overlay(self, weapon_index):
        weapon_bg_rect = self.selection_box(10, 600, active=True)
        # guard index
        if weapon_index < 0 or weapon_index >= len(self.weapon_graphics):
            return
        weapon_surf = self.weapon_graphics[weapon_index]
        # scale weapon to fit the box while keeping aspect ratio
        w, h = weapon_surf.get_size()
        if w > item_box_size or h > item_box_size:
            scale = min(item_box_size / w, item_box_size / h)
            new_size = (max(1, int(w * scale)), max(1, int(h * scale)))
            weapon_surf = pygame.transform.scale(weapon_surf, new_size)
        weapon_rect = weapon_surf.get_rect(center=weapon_bg_rect.center)
        self.display_surface.blit(weapon_surf, weapon_rect)    

    def magic_overlay(self, magic_index):
        magic_bg_rect = self.selection_box(100, 600, active=True)
        # guard index
        if magic_index < 0 or magic_index >= len(self.magic_graphics):
            return
        magic_surf = self.magic_graphics[magic_index]
        # scale magic icon to fit the box while keeping aspect ratio
        w, h = magic_surf.get_size()
        if w > item_box_size or h > item_box_size:
            scale = min(item_box_size / w, item_box_size / h)
            new_size = (max(1, int(w * scale)), max(1, int(h * scale)))
            magic_surf = pygame.transform.scale(magic_surf, new_size)
        magic_rect = magic_surf.get_rect(center=magic_bg_rect.center)
        self.display_surface.blit(magic_surf, magic_rect)

    def show_exp(self, exp):
        text_surf = self.font.render(f'Exp: {exp}', False, text_color)
        text_rect = text_surf.get_rect(topleft=(10, 60))

        pygame.draw.rect(self.display_surface, ui_bg_color, text_rect)
        self.display_surface.blit(text_surf, text_rect)

    def display(self, player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, health_color)
        self.show_bar(player.energy, player.stats['energy'], self.magic_bar_rect, energy_color)

        self.show_exp(player.exp)
        
        self.weapon_overlay(player.weapon_index)
        self.magic_overlay(player.magic_index)
        