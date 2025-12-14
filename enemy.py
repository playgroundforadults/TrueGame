import pygame
from settings import *
from entity import Entity

class Enemy(Entity):
    def __init__(self, monster_name, pos, groups):
        # initialize base class and register with any provided groups
        super().__init__(*groups)
        self.sprite_type = 'enemy'

        # simple placeholder enemy image
        self.image = pygame.Surface((64, 64), flags=pygame.SRCALPHA)
        self.image.fill((120, 20, 20))
        self.rect = self.image.get_rect(topleft=pos)

        # basic hitbox for sorting and collisions
        self.hitbox = self.rect.copy()