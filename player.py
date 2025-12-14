import pygame
from settings import *
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack, create_magic):
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

        self.import_player_assets()
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.15
        

        self.direction = pygame.math.Vector2()
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.obstacle_sprites = obstacle_sprites

        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 1
        self.weapon = list(weapons_data.keys())[self.weapon_index]

        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.switch_magic_time = None

        self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 6}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.exp = 123
        self.speed = self.stats['speed']


    def import_player_assets(self):
        character_path = 'graphics/player/'
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [], 'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [], 'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': []}
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
        
    def get_status(self):
        # Normalize base direction (remove any suffixes)
        base = self.status
        if base.endswith('_idle'):
            base = base.replace('_idle', '')
        if base.endswith('_attack'):
            base = base.replace('_attack', '')

        # If moving, update base facing direction
        if self.direction.x != 0 or self.direction.y != 0:
            if abs(self.direction.x) > 0:
                base = 'left' if self.direction.x < 0 else 'right'
            elif abs(self.direction.y) > 0:
                base = 'up' if self.direction.y < 0 else 'down'

        # Lock out movement while attacking
        if self.attacking:
            # ensure no movement while attacking
            self.direction.x = 0
            self.direction.y = 0
            self.status = f"{base}_attack"
        else:
            # No attack: set either moving or idle status
            if self.direction.x != 0 or self.direction.y != 0:
                self.status = base
            else:
                self.status = f"{base}_idle"
        

    def input(self):
        if not self.attacking:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'
            elif keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
            else:
                self.direction.x = 0

            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
        
            if keys[pygame.K_LCTRL]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[self.magic_index]
                strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
                cost = list(magic_data.values())[self.magic_index]['cost']
                self.create_magic(style, strength, cost)

            if keys[pygame.K_e]:
                self.magic_index += 1
                if self.magic_index >= len(magic_data):
                    self.magic_index = 0
                self.magic = list(magic_data.keys())[self.magic_index]
                pygame.time.delay(200)  # simple debounce to prevent rapid switching
            
            if keys[pygame.K_q]:
                self.weapon_index += 1
                if self.weapon_index >= len(weapons_data):
                    self.weapon_index = 0
                self.weapon = list(weapons_data.keys())[self.weapon_index]
                pygame.time.delay(200)  # simple debounce to prevent rapid switching
     

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

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.destroy_attack()

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(midbottom=self.hitbox.midbottom)

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)