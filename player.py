import pygame
from settings import *
from support import import_folder
from entity import Entity

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack, create_magic):
        super().__init__(*groups)
        self.image = pygame.image.load('images/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        
        # ok so this makes the position a vector for more precise movement
        self.pos = pygame.math.Vector2(self.rect.topleft)
        # create a hitbox smaller than the sprite rect for better collisions
        hit_w = int(self.rect.width * 0.5)
        hit_h = int(self.rect.height * 0.35)
        self.hitbox = pygame.Rect(0, 0, hit_w, hit_h)
        self.hitbox.centerx = self.rect.centerx
        self.hitbox.bottom = self.rect.bottom


        #player visual stuff
        self.import_player_assets()
        self.status = 'down'
                
        #the stuff that makes these goofy pixels move
        self.direction = pygame.math.Vector2()
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.obstacle_sprites = obstacle_sprites

        #weapon
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 1
        self.weapon = list(weapons_data.keys())[self.weapon_index]

        #we love casting spells
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.switch_magic_time = None

        # stat
        self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 6}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.exp = 0
        self.level = 1
        self.exp_needed = 100
        self.speed = self.stats['speed']
        
        #i frames
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500


    def import_player_assets(self):
        character_path = 'graphics/player/'
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [], 'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [], 'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': []}
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
        
    def get_status(self):
        base = self.status
        if base.endswith('_idle'):
            base = base.replace('_idle', '')
        if base.endswith('_attack'):
            base = base.replace('_attack', '')

        if self.direction.x != 0 or self.direction.y != 0:
            if abs(self.direction.x) > 0:
                base = 'left' if self.direction.x < 0 else 'right'
            elif abs(self.direction.y) > 0:
                base = 'up' if self.direction.y < 0 else 'down'

        # no moving while attacking
        if self.attacking:
            # ensure no movement while attacking
            self.direction.x = 0
            self.direction.y = 0
            self.status = f"{base}_attack"
        else:
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
     
    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']
        weapon_damage = weapons_data[self.weapon]['damage']
        return base_damage + weapon_damage
    
    def check_death(self):
        if self.health <= 0:
            self.kill()

    def get_damage(self, amount):
        if self.vulnerable:
            self.health -= amount
            self.vulnerable = False
            self.hurt_time = pygame.time.get_ticks()

    def check_level_up(self):
        if self.exp >= self.exp_needed:
            self.exp -= self.exp_needed
            self.level += 1
            self.exp_needed = int(self.exp_needed * 1.1) + 50 # Increase requirement
            
            # stat boost when leveling
            self.stats['health'] += 10
            self.stats['energy'] += 5
            self.stats['attack'] += 2
            self.stats['magic'] += 1
            
            #health pack from leveling
            self.health = self.stats['health']
            self.energy = self.stats['energy']
            print(f"Leveled up to {self.level}!")

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.destroy_attack()
        
        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

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
        self.check_level_up()
        self.check_death()