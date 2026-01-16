import pygame
from settings import *
from support import import_folder
from entity import Entity

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack, create_magic):
        # Initializes the parent Entity class.
        super().__init__(*groups)
        # Loads the default player image.
        self.image = pygame.image.load('images/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        
        # Uses a vector for precise sub-pixel position tracking.
        self.pos = pygame.math.Vector2(self.rect.topleft)
        
        # Creates a custom hitbox that is smaller than the sprite for better collision feel (feet only).
        hit_w = int(self.rect.width * 0.5)
        hit_h = int(self.rect.height * 0.35)
        self.hitbox = pygame.Rect(0, 0, hit_w, hit_h)
        self.hitbox.centerx = self.rect.centerx
        self.hitbox.bottom = self.rect.bottom

        # Loads all player animation frames.
        self.import_player_assets()
        self.status = 'down'
                
        # Movement and attack state variables.
        self.direction = pygame.math.Vector2()
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.obstacle_sprites = obstacle_sprites

        # References to callback functions for creating/destroying weapon attacks.
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 1
        self.weapon = list(weapons_data.keys())[self.weapon_index]

        # References and state for magic system.
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.switch_magic_time = None

        # Player RPG statistics.
        self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 6}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.exp = 0
        self.level = 1
        self.exp_needed = 100
        self.speed = self.stats['speed']
        
        # Invincibility frame logic.
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500


    def import_player_assets(self):
        # Defines the base path for player graphics.
        character_path = 'graphics/player/'
        # Dictionary keys correspond to folder names for each animation state.
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [], 'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [], 'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': []}
        
        # Iterates through keys and imports images from the corresponding folder.
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
        
    def get_status(self):
        # Determines the current status string (e.g., 'left_idle', 'up_attack') based on movement and action.
        
        # If the player is not moving, set status to idle.
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'

        # If attacking, movement is locked and status is set to attack.
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            # If not attacking, remove '_attack' suffix.
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')

    def input(self):
        # Handles keyboard input.
        if not self.attacking:
            keys = pygame.key.get_pressed()

            # Vertical movement
            if keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            # Horizontal movement
            if keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'
            elif keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
            else:
                self.direction.x = 0

            # Attack input (Spacebar)
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
        
            # Magic input (Left Control)
            if keys[pygame.K_LCTRL]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[self.magic_index]
                strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
                cost = list(magic_data.values())[self.magic_index]['cost']
                self.create_magic(style, strength, cost)

            # Switch magic input (E)
            if keys[pygame.K_e]:
                self.magic_index += 1
                if self.magic_index >= len(magic_data):
                    self.magic_index = 0
                self.magic = list(magic_data.keys())[self.magic_index]
                pygame.time.delay(200)  # Simple debounce
            
            # Switch weapon input (Q)
            if keys[pygame.K_q]:
                self.weapon_index += 1
                if self.weapon_index >= len(weapons_data):
                    self.weapon_index = 0
                self.weapon = list(weapons_data.keys())[self.weapon_index]
                pygame.time.delay(200)  # Simple debounce
     
    def get_full_weapon_damage(self):
        # Calculates total damage = base attack + weapon damage.
        base_damage = self.stats['attack']
        weapon_damage = weapons_data[self.weapon]['damage']
        return base_damage + weapon_damage
    
    def check_death(self):
        # Kills the player sprite if health drops to 0.
        if self.health <= 0:
            self.kill()

    def get_damage(self, amount):
        # Applies damage to the player if they are not currently invulnerable.
        if self.vulnerable:
            self.health -= amount
            self.vulnerable = False
            self.hurt_time = pygame.time.get_ticks()

    def check_level_up(self):
        # Checks if current EXP exceeds the requirement for the next level.
        if self.exp >= self.exp_needed:
            self.exp -= self.exp_needed
            self.level += 1
            self.exp_needed = int(self.exp_needed * 1.1) + 50 # Increases difficulty curve
            
            # Boosts stats upon leveling up.
            self.stats['health'] += 10
            self.stats['energy'] += 5
            self.stats['attack'] += 2
            self.stats['magic'] += 1
            
            # Restores health and energy to new max.
            self.health = self.stats['health']
            self.energy = self.stats['energy']
            print(f"Leveled up to {self.level}!")

    def cooldowns(self):
        # Manages timing for attacks and invulnerability.
        current_time = pygame.time.get_ticks()
        
        if self.attacking:
            # End attack state if cooldown has passed.
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.destroy_attack()
        
        if not self.vulnerable:
            # End invulnerability if duration has passed.
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

    def animate(self):
        # Cycles through frames of the current animation status.
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(midbottom=self.hitbox.midbottom)

    def update(self):
        # Main update loop for the player.
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
        self.check_level_up()
        self.check_death()