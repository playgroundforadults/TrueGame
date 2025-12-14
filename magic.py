import pygame
from settings import *
from support import import_folder
from random import randint

class MagicPlayer:
    def __init__(self, animation_player):
        self.animation_player = animation_player
        self.frames = {
            'flame': import_folder('graphics/particles/flame/frames'),
            'aura': import_folder('graphics/particles/aura'),
            'heal': import_folder('graphics/particles/heal/frames'),
        }

    def heal(self, player, strength, cost, groups):
        if player.energy >= cost:
            player.health += strength
            player.energy -= cost
            if player.health >= player.stats['health']:
                player.health = player.stats['health']
            
            # Spawn particles
            self.animation_player.create_particles('aura', player.rect.center, groups)
            self.animation_player.create_particles('heal', player.rect.center + pygame.math.Vector2(0, -60), groups)

    def flame(self, player, cost, groups):
        if player.energy >= cost:
            player.energy -= cost
            
            # Determine direction for flame
            if player.status.split('_')[0] == 'right': direction = pygame.math.Vector2(1, 0)
            elif player.status.split('_')[0] == 'left': direction = pygame.math.Vector2(-1, 0)
            elif player.status.split('_')[0] == 'up': direction = pygame.math.Vector2(0, -1)
            else: direction = pygame.math.Vector2(0, 1)

            # Spawn multiple flame particles to create a "throw" effect
            for i in range(1, 6):
                if direction.x: # Horizontal
                    offset_x = (direction.x * i) * tile_size
                    x = player.rect.centerx + offset_x + randint(-tile_size // 3, tile_size // 3)
                    y = player.rect.centery + randint(-tile_size // 3, tile_size // 3)
                    self.animation_player.create_particles('flame', (x, y), groups)
                else: # Vertical
                    offset_y = (direction.y * i) * tile_size
                    x = player.rect.centerx + randint(-tile_size // 3, tile_size // 3)
                    y = player.rect.centery + offset_y + randint(-tile_size // 3, tile_size // 3)
                    self.animation_player.create_particles('flame', (x, y), groups)

class AnimationPlayer:
    def __init__(self):
        self.frames = {
            # Magic
            'flame': import_folder('graphics/particles/flame/frames'),
            'aura': import_folder('graphics/particles/aura'),
            'heal': import_folder('graphics/particles/heal/frames'),
            
            # Attacks
            'leaf_attack': import_folder('graphics/particles/leaf_attack'),
            'claw': import_folder('graphics/particles/claw'),
            'slash': import_folder('graphics/particles/slash'),
            'sparkle': import_folder('graphics/particles/sparkle'),
            'thunder': import_folder('graphics/particles/thunder'),

            # Monster deaths / smoke
            'squid': import_folder('graphics/particles/smoke2'),
            'raccoon': import_folder('graphics/particles/raccoon'),
            'spirit': import_folder('graphics/particles/nova'),
            'bamboo': import_folder('graphics/particles/bamboo'),
            
            # Grass Particles
            'leaf1': import_folder('graphics/particles/leaf1'),
            'leaf2': import_folder('graphics/particles/leaf2'),
            'leaf3': import_folder('graphics/particles/leaf3'),
            'leaf4': import_folder('graphics/particles/leaf4'),
            'leaf5': import_folder('graphics/particles/leaf5'),
            'leaf6': import_folder('graphics/particles/leaf6'),
        }
    
    def create_particles(self, animation_type, pos, groups):
        animation_frames = self.frames[animation_type]
        ParticleEffect(pos, animation_frames, groups)

class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, animation_frames, groups):
        super().__init__(groups)
        self.sprite_type = 'magic'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()