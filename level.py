import pygame
from settings import *

from tile import Tile
from player import Player
from support import *
from random import choice

class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        # Use a camera-aware group so we can render sprites relative to the player's position
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.create_map()

    
    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('map/map_Grass.csv'),
            'object': import_csv_layout('map/map_Objects.csv')
        }
        graphics = {
            'grass': import_folder('graphics/Grass'),
            'object': import_folder('graphics/Objects')
        }
        
        # iterate each layous, and create Tiles where the CSV indicates a tile
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    x = col_index * tile_size
                    y = row_index * tile_size
                    if style == 'boundary' and col != '-1':
                        Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'invisible')
                    if style == 'grass' and col != '-1':
                        random_grass_image = choice(graphics['grass'])
                        Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'grass', random_grass_image)
                    if style == 'object' and col != '-1':
                        object_image = graphics['object'][int(col)]
                        Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', object_image)
                    
        self.player = Player((2000, 1500), [self.visible_sprites], self.obstacle_sprites)

    def run(self):
        # Update all sprites, then draw them using the camera offset
        self.visible_sprites.update()
        self.visible_sprites.custom_draw(self.player)


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        #load the floor image
        self.floor_surface = pygame.image.load("graphics/tilemap/ground.png").convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))


    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        # Sort by hitbox Y if available (player or entity foot position), otherwise fall back to rect.centery
        def sort_key(sprite):
            if hasattr(sprite, 'hitbox'):
                return sprite.hitbox.centery
            return sprite.rect.centery
        
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=sort_key):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)