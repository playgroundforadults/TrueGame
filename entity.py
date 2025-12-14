import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()

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