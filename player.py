import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(*groups)
        self.image = pygame.image.load('images/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        
        # ok so this makes the position a vector for more precise movement
        self.pos = pygame.math.Vector2(self.rect.topleft)
        # Hitbox used for collisions and sorting; anchored at player's feet
        hit_w = int(self.rect.width * 0.5)
        hit_h = int(self.rect.height * 0.35)
        self.hitbox = pygame.Rect(0, 0, hit_w, hit_h)
        self.hitbox.centerx = self.rect.centerx
        self.hitbox.bottom = self.rect.bottom

        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.obstacle_sprites = obstacle_sprites

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        dx = self.direction.x * speed
        dy = self.direction.y * speed

        # Horizontal movement using hitbox for collisions
        self.pos.x += dx
        self.hitbox.x = round(self.pos.x)
        for sprite in self.obstacle_sprites:
            if sprite.rect.colliderect(self.hitbox):
                if dx > 0:  # moving right
                    self.hitbox.right = sprite.rect.left
                if dx < 0:  # moving left
                    self.hitbox.left = sprite.rect.right
                self.pos.x = self.hitbox.x

        # Vertical movement using hitbox for collisions
        self.pos.y += dy
        self.hitbox.y = round(self.pos.y)
        for sprite in self.obstacle_sprites:
            if sprite.rect.colliderect(self.hitbox):
                if dy > 0:  # moving down
                    self.hitbox.bottom = sprite.rect.top
                if dy < 0:  # moving up
                    self.hitbox.top = sprite.rect.bottom
                self.pos.y = self.hitbox.y

        # keep the visual rect aligned with the hitbox feet area
        self.rect.midbottom = self.hitbox.midbottom




    def update(self):
        self.input()
        self.move(self.speed)