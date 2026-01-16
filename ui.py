import pygame
from settings import *

class UI:
    def __init__(self):
        # Gets a reference to the main display surface.
        self.display_surface = pygame.display.get_surface()
        # Creates a font object for general UI text.
        self.font = pygame.font.Font(ui_font, ui_font_size)
        # Creates a larger font object specifically for the victory message.
        self.victory_font = pygame.font.Font(ui_font, 50)

        # Defines the rectangle for the health bar background.
        self.health_bar_rect = pygame.Rect(10, 10, health_bar_width, bar_height)
        # Defines the rectangle for the magic/energy bar background.
        self.magic_bar_rect = pygame.Rect(10, 34, magic_bar_width, bar_height)

        # Pre-loads all weapon images to be displayed in the UI overlay.
        self.weapon_graphics = []
        for weapon in weapons_data.values():
            path = weapon['graphic']
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)
        
        # Pre-loads all magic spell images to be displayed in the UI overlay.
        self.magic_graphics = []
        for magic in magic_data.values():
            path = magic['graphic']
            magic_surf = pygame.image.load(path).convert_alpha()
            self.magic_graphics.append(magic_surf)


    def show_bar(self, current, max_amount, bg_rect, color):
        # Draws the background of the bar (empty state).
        self.display_surface.fill(ui_bg_color, bg_rect)
        
        # Calculates the width of the filled portion based on the current/max ratio.
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        
        # Creates a rectangle for the filled portion.
        current_rect = bg_rect.copy()
        current_rect.width = current_width
        
        # Draws the filled portion of the bar in the specified color.
        self.display_surface.fill(color, current_rect)
        pygame.draw.rect(self.display_surface, color, current_rect)

        # Draws a border around the bar.
        pygame.draw.rect(self.display_surface, ui_border_color, bg_rect, 3)

    def selection_box(self, left, top, active=False):
        # Defines the rectangle for a selection box (weapon/magic slot).
        bg_rect = pygame.Rect(left, top, item_box_size, item_box_size)
        # Fills the box with the UI background color.
        pygame.draw.rect(self.display_surface, ui_bg_color, bg_rect)
        # Determines the border color: gold if active, standard dark grey otherwise.
        border_color = ui_border_color_active if active else ui_border_color
        # Draws the border around the selection box.
        pygame.draw.rect(self.display_surface, border_color, bg_rect, 3)
        return bg_rect

    def weapon_overlay(self, weapon_index):
        # Draws the selection box for the weapon slot.
        weapon_bg_rect = self.selection_box(10, 600, active=True)
        # Ensures the index is valid to prevent crashes.
        if weapon_index < 0 or weapon_index >= len(self.weapon_graphics):
            return
        
        # Retrieves the image for the currently selected weapon.
        weapon_surf = self.weapon_graphics[weapon_index]
        
        # Scales the weapon image to fit inside the box while maintaining aspect ratio.
        w, h = weapon_surf.get_size()
        if w > item_box_size or h > item_box_size:
            scale = min(item_box_size / w, item_box_size / h)
            new_size = (max(1, int(w * scale)), max(1, int(h * scale)))
            weapon_surf = pygame.transform.scale(weapon_surf, new_size)
        
        # Centers the weapon image within the selection box.
        weapon_rect = weapon_surf.get_rect(center=weapon_bg_rect.center)
        # Blits the weapon image onto the screen.
        self.display_surface.blit(weapon_surf, weapon_rect)    

    def magic_overlay(self, magic_index):
        # Draws the selection box for the magic slot.
        magic_bg_rect = self.selection_box(100, 600, active=True)
        # Ensures the index is valid.
        if magic_index < 0 or magic_index >= len(self.magic_graphics):
            return
        
        # Retrieves the image for the currently selected magic.
        magic_surf = self.magic_graphics[magic_index]
        
        # Scales the magic image to fit inside the box while maintaining aspect ratio.
        w, h = magic_surf.get_size()
        if w > item_box_size or h > item_box_size:
            scale = min(item_box_size / w, item_box_size / h)
            new_size = (max(1, int(w * scale)), max(1, int(h * scale)))
            magic_surf = pygame.transform.scale(magic_surf, new_size)
        
        # Centers the magic image within the selection box.
        magic_rect = magic_surf.get_rect(center=magic_bg_rect.center)
        # Blits the magic image onto the screen.
        self.display_surface.blit(magic_surf, magic_rect)

    def show_exp(self, exp):
        # Renders the experience text.
        text_surf = self.font.render(f'Exp: {exp}', False, text_color)
        # Positions the text on the screen below the bars.
        text_rect = text_surf.get_rect(topleft=(10, 60))

        # Draws a background box for the text to make it readable.
        pygame.draw.rect(self.display_surface, ui_bg_color, text_rect)
        # Blits the text onto the screen.
        self.display_surface.blit(text_surf, text_rect)
    
    def display_victory_message(self):
        # Renders the "VICTORY!" text using the large font.
        text_surf = self.victory_font.render('VICTORY!', False, text_color)
        # Centers the text on the screen.
        text_rect = text_surf.get_rect(center = (width / 2, height / 2))
        
        # Draws a box background behind the text.
        pygame.draw.rect(self.display_surface, ui_bg_color, text_rect.inflate(20, 20))
        # Draws a border around the victory message box.
        pygame.draw.rect(self.display_surface, ui_border_color, text_rect.inflate(20, 20), 3)
        # Blits the victory text onto the screen.
        self.display_surface.blit(text_surf, text_rect)

    def display(self, player):
        # Main method called every frame to draw all UI elements.
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, health_color)
        self.show_bar(player.energy, player.stats['energy'], self.magic_bar_rect, energy_color)

        self.show_exp(player.exp)
        
        self.weapon_overlay(player.weapon_index)
        self.magic_overlay(player.magic_index)