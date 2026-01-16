import pygame

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        # Initializes the weapon sprite and adds it to the relevant groups (visible and attack sprites).
        super().__init__(groups)
        # Identifies this sprite as a weapon for collision logic.
        self.sprite_type = 'weapon'
        
        # Determines the direction the player is facing to orient the weapon correctly.
        direction = player.status.split('_')[0]

        # Constructs the file path for the weapon image based on the player's current weapon and direction.
        full_path = f'graphics/weapons/{player.weapon}/{direction}.png'
        # Loads the weapon image.
        self.image = pygame.image.load(full_path).convert_alpha()
        
        # Positions the weapon relative to the player based on direction.
        if direction == 'right':
            # If facing right, place weapon on the right side of the player.
            self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0, 16))
        elif direction == 'left':
            # If facing left, place weapon on the left side of the player.
            self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(0, 16))
        elif direction == 'down':
            # If facing down, place weapon below the player.
            self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(-10, 0))
        else:
            # If facing up, place weapon above the player.
            self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(-10, 0))