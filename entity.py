import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, *groups):
        # Initializes the parent Sprite class with any provided groups.
        super().__init__(*groups)
        # Sets the starting index for animation frames.
        self.frame_index = 0
        # Defines how fast the animation frames cycle.
        self.animation_speed = 0.15
        # Creates a Vector2 to represent the entity's movement direction.
        self.direction = pygame.math.Vector2()

    def move(self, speed):
        # Checks if the entity is moving diagonally (magnitude not 0 or 1).
        if self.direction.magnitude() != 0:
            # Normalizes the vector to ensure consistent speed in all directions.
            self.direction = self.direction.normalize()
        
        # Calculates the displacement in X and Y based on speed and direction.
        dx = self.direction.x * speed
        dy = self.direction.y * speed

        # Moves the entity horizontally.
        self.pos.x += dx
        # Updates the hitbox's x-coordinate to match the new position.
        self.hitbox.x = round(self.pos.x)
        # Checks for collisions with any obstacles in the horizontal direction.
        for sprite in self.obstacle_sprites:
            if sprite.rect.colliderect(self.hitbox):
                # If moving right and colliding, snap hitbox right side to obstacle left side.
                if dx > 0:
                    self.hitbox.right = sprite.rect.left
                # If moving left and colliding, snap hitbox left side to obstacle right side.
                if dx < 0:
                    self.hitbox.left = sprite.rect.right
                # Updates the precise position vector to match the collision resolution.
                self.pos.x = self.hitbox.x

        # Moves the entity vertically.
        self.pos.y += dy
        # Updates the hitbox's y-coordinate to match the new position.
        self.hitbox.y = round(self.pos.y)
        # Checks for collisions with any obstacles in the vertical direction.
        for sprite in self.obstacle_sprites:
            if sprite.rect.colliderect(self.hitbox):
                # If moving down and colliding, snap hitbox bottom to obstacle top.
                if dy > 0:
                    self.hitbox.bottom = sprite.rect.top
                # If moving up and colliding, snap hitbox top to obstacle bottom.
                if dy < 0:
                    self.hitbox.top = sprite.rect.bottom
                # Updates the precise position vector to match the collision resolution.
                self.pos.y = self.hitbox.y

        # Aligns the visual sprite rect to the bottom center of the hitbox.
        # This creates a "depth" effect where the entity stands on the ground.
        self.rect.midbottom = self.hitbox.midbottom