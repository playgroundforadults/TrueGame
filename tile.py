import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface=None):
        super().__init__(*groups)
        self.sprite_type = sprite_type

        # Choose image based on sprite_type. If a surface is provided use it.
        if surface is not None:
            self.image = pygame.transform.scale(surface, (tile_size, tile_size))
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
                self.image = pygame.transform.scale(self.image, (tile_size, tile_size))

        self.rect = self.image.get_rect(topleft=pos)