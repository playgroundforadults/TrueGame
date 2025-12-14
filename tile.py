import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface=None):
        # Initializes the sprite and adds it to the specified groups.
        super().__init__(*groups)
        # Stores the type of tile (e.g., 'grass', 'object', 'invisible').
        self.sprite_type = sprite_type

        # Determines the visual image for the tile.
        if surface is not None:
            # If a specific image surface is passed, use it directly.
            self.image = surface
        else:
            # If no surface is provided, handle based on sprite_type.
            if sprite_type == 'invisible':
                # Create a transparent surface for invisible collision blocks.
                self.image = pygame.Surface((tile_size, tile_size), flags=pygame.SRCALPHA)
                self.image.fill((0, 0, 0, 0))
            else:
                # Default logic for other types (like obstacles).
                img_path = 'images/rock.png'
                try:
                    # Attempt to load the rock image.
                    self.image = pygame.image.load(img_path).convert_alpha()
                except Exception:
                    # Fallback to a magenta square if the image fails to load.
                    self.image = pygame.Surface((tile_size, tile_size))
                    self.image.fill((255, 0, 255))
        
        # Creates a rectangle representing the grid cell this tile occupies.
        grid_rect = pygame.Rect(pos, (tile_size, tile_size))

        # Calculates the position of the image.
        img_rect = self.image.get_rect()
        if img_rect.width == tile_size and img_rect.height == tile_size:
            # If the image matches the tile size exactly, place it at the top-left of the position.
            self.rect = img_rect.move(pos)
        else:
            # If the image is larger (like a tree), align its bottom with the bottom of the tile grid.
            # This ensures proper layering and perspective.
            midx = pos[0] + tile_size // 2
            bottom = pos[1] + tile_size
            self.rect = img_rect
            self.rect.midbottom = (midx, bottom)

        # Creates a hitbox for collisions that is slightly shorter than the grid rect.
        # This allows for some overlap at the top, creating a pseudo-3D effect.
        self.hitbox = grid_rect.inflate(0, -10)