import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface=None):
        super().__init__(*groups)
        self.sprite_type = sprite_type

        # Choose image based on sprite_type. If a surface is provided, use it as-is.
        if surface is not None:
            self.image = surface
        else:
            if sprite_type == 'invisible':
                self.image = pygame.Surface((tile_size, tile_size), flags=pygame.SRCALPHA)
                self.image.fill((0, 0, 0, 0))
            else:
                # default to rock for obstacle tiles, can expand mapping later
                img_path = 'images/rock.png'
                try:
                    self.image = pygame.image.load(img_path).convert_alpha()
                except Exception:
                    # fallback to a plain surface if image missing
                    self.image = pygame.Surface((tile_size, tile_size))
                    self.image.fill((255, 0, 255))
                # Keep the original loaded image size; don't scale automatically

        # grid rect is the tile-sized cell where this tile lives; used for collisions
        grid_rect = pygame.Rect(pos, (tile_size, tile_size))

        # Position the sprite image: if it's the same size as the tile, place topleft at pos.
        # If it's taller/wider, anchor its bottom to the tile bottom so it 'sits' on the tile.
        img_rect = self.image.get_rect()
        if img_rect.width == tile_size and img_rect.height == tile_size:
            self.rect = img_rect.move(pos)
        else:
            # center horizontally on the tile and anchor the bottom to the tile bottom
            midx = pos[0] + tile_size // 2
            bottom = pos[1] + tile_size
            self.rect = img_rect
            self.rect.midbottom = (midx, bottom)

        # Use the grid rect for collisions (slightly shrunk vertically)
        self.hitbox = grid_rect.inflate(0, -10)