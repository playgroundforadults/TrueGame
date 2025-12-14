import pygame
from settings import *
from support import import_folder
from random import randint

class MagicPlayer:
    def __init__(self, animation_player):
        # Stores a reference to the animation player to spawn visual effects.
        self.animation_player = animation_player
        # Loads animation frames for different magic types.
        self.frames = {
            'flame': import_folder('graphics/particles/flame/frames'),
            'aura': import_folder('graphics/particles/aura'),
            'heal': import_folder('graphics/particles/heal/frames'),
            'leaf': import_folder('graphics/particles/leaf_attack')
        }

    def heal(self, player, strength, cost, groups):
        # Checks if the player has enough energy to cast the spell.
        if player.energy >= cost:
            # Applies the healing strength to the player's health.
            player.health += strength
            # Deducts the energy cost.
            player.energy -= cost
            # Caps health at the maximum stat value.
            if player.health >= player.stats['health']:
                player.health = player.stats['health']
            
            # Spawns 'aura' particles at the player's center.
            self.animation_player.create_particles('aura', player.rect.center, groups)
            # Spawns 'heal' particles slightly above the player.
            self.animation_player.create_particles('heal', player.rect.center + pygame.math.Vector2(0, -60), groups)

    def flame(self, player, cost, groups):
        # Checks if the player has enough energy.
        if player.energy >= cost:
            # Deducts the energy cost.
            player.energy -= cost
            
            # Determines the direction the player is facing to throw the flame.
            if player.status.split('_')[0] == 'right': direction = pygame.math.Vector2(1, 0)
            elif player.status.split('_')[0] == 'left': direction = pygame.math.Vector2(-1, 0)
            elif player.status.split('_')[0] == 'up': direction = pygame.math.Vector2(0, -1)
            else: direction = pygame.math.Vector2(0, 1)

            # Spawns multiple flame particles in a line to simulate a flamethrower effect.
            for i in range(1, 6):
                if direction.x: # Horizontal throw
                    offset_x = (direction.x * i) * tile_size
                    # Adds randomness to position for a natural fire look.
                    x = player.rect.centerx + offset_x + randint(-tile_size // 3, tile_size // 3)
                    y = player.rect.centery + randint(-tile_size // 3, tile_size // 3)
                    self.animation_player.create_particles('flame', (x, y), groups)
                else: # Vertical throw
                    offset_y = (direction.y * i) * tile_size
                    x = player.rect.centerx + randint(-tile_size // 3, tile_size // 3)
                    y = player.rect.centery + offset_y + randint(-tile_size // 3, tile_size // 3)
                    self.animation_player.create_particles('flame', (x, y), groups)

class AnimationPlayer:
    def __init__(self):
        # Loads all particle animation frames into a dictionary.
        self.frames = {
            # Magic effects
            'flame': import_folder('graphics/particles/flame/frames'),
            'aura': import_folder('graphics/particles/aura'),
            'heal': import_folder('graphics/particles/heal/frames'),
            
            # Attack impacts
            'leaf_attack': import_folder('graphics/particles/leaf_attack'),
            'claw': import_folder('graphics/particles/claw'),
            'slash': import_folder('graphics/particles/slash'),
            'sparkle': import_folder('graphics/particles/sparkle'),
            'thunder': import_folder('graphics/particles/thunder'),

            # Monster death/despawn effects
            'squid': import_folder('graphics/particles/smoke2'),
            'raccoon': import_folder('graphics/particles/raccoon'),
            'spirit': import_folder('graphics/particles/nova'),
            'bamboo': import_folder('graphics/particles/bamboo'),
            
            # Grass destruction particles (leaf variations)
            'leaf1': import_folder('graphics/particles/leaf1'),
            'leaf2': import_folder('graphics/particles/leaf2'),
            'leaf3': import_folder('graphics/particles/leaf3'),
            'leaf4': import_folder('graphics/particles/leaf4'),
            'leaf5': import_folder('graphics/particles/leaf5'),
            'leaf6': import_folder('graphics/particles/leaf6'),
        }
    
    def create_particles(self, animation_type, pos, groups):
        # Retrieves the frames for the requested animation type.
        animation_frames = self.frames[animation_type]
        # Creates a ParticleEffect sprite at the given position.
        ParticleEffect(pos, animation_frames, groups)

class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, animation_frames, groups):
        # Initializes the particle sprite.
        super().__init__(groups)
        self.sprite_type = 'magic'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        # Sets the initial image.
        self.image = self.frames[self.frame_index]
        # Centers the rect at the spawn position.
        self.rect = self.image.get_rect(center = pos)

    def animate(self):
        # Increments the frame index.
        self.frame_index += self.animation_speed
        # If the animation finishes, remove the sprite.
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            # Otherwise update the image to the current frame.
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        # Called every frame to run the animation logic.
        self.animate()