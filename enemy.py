import pygame
from settings import *
from entity import Entity
from support import import_folder

class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacle_sprites, add_exp):
        # Initialize the base Entity class and register with sprite groups.
        super().__init__(*groups)
        self.sprite_type = 'enemy'

        # Load graphics specific to the monster name.
        self.import_graphics(monster_name)
        self.status = 'idle'

        # Set the initial image based on the first frame of the idle animation.
        if self.animations.get(self.status) and len(self.animations[self.status]) > 0:
            self.image = self.animations[self.status][int(self.frame_index)]
        else:
            # Fallback placeholder (red square) if graphics are missing.
            self.image = pygame.Surface((64, 64), flags=pygame.SRCALPHA)
            self.image.fill((120, 20, 20))

        # Setup the rectangle and hitbox for the enemy.
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
        # Position vector for smooth movement calculations.
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.obstacle_sprites = obstacle_sprites

        # Action state variables.
        self.attacking = False
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 1000

        # Load specific stats from the monster_data dictionary in settings.py.
        self.monster_name = monster_name 
        monster_info = monster_data[self.monster_name] 
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_type']
        
        # Override default cooldown if specified in monster data.
        if 'attack_cooldown' in monster_info:
            self.attack_cooldown = monster_info['attack_cooldown']

        # Logic for taking damage and invincibility frames.
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300
        
        # Logic for hit stun (knockback state).
        self.hit_stun = False
        self.hit_stun_duration = 300
        
        # Reference to the function for adding experience to the player.
        self.add_exp = add_exp
    
    def actions(self):
        # Prevent the enemy from starting an attack if they are currently stunned.
        if self.hit_stun:
            return

        # Determines if the enemy should attack based on status and cooldown.
        if self.status == 'attack' and self.can_attack and not self.attacking:
            print('attack')
            self.can_attack = False
            self.attack_time = pygame.time.get_ticks()
            self.attacking = True

    def get_damage(self, player, attack_type):
        # Called when the player hits the enemy.
        if self.vulnerable:
            # Calculate damage based on the source (weapon or magic).
            if attack_type == 'weapon':
                self.health -= player.get_full_weapon_damage()
            else:
                magic_damage = player.stats['magic'] + magic_data[player.magic]['strength']
                self.health -= magic_damage
            
            # Record the hit time and make the enemy temporarily invulnerable.
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False
            
            # Trigger hit stun to interrupt actions and allow knockback.
            self.hit_stun = True
            self.attacking = False

    def check_death(self):
        # Checks if health is zero or less, grants EXP, and removes the sprite.
        if self.health <= 0:
            self.add_exp(self.exp)
            self.kill()

    def cooldowns(self):
        # Manages various timers.
        current_time = pygame.time.get_ticks()
        
        # Attack cooldown reset.
        if not self.can_attack and self.attack_time is not None:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
                self.attack_time = None
        
        # Invincibility frame reset.
        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

        # Hit stun (knockback) reset.
        if self.hit_stun:
            if current_time - self.hit_time >= self.hit_stun_duration:
                self.hit_stun = False

    def import_graphics(self, name):
        # Loads animation frames for idle, move, and attack states.
        self.animations = {'idle': [], 'move': [], 'attack': []}
        main_path = f'graphics/monsters/{name}/'
        for animation in self.animations.keys():
            full_path = main_path + animation
            self.animations[animation] = import_folder(main_path + animation)

    def animate(self):
        # Handles sprite animation cycling.
        animation = self.animations[self.status]
        if not animation:
            return
            
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            # If an attack animation finishes, stop the attacking state.
            if self.status == 'attack':
                self.attacking = False
            self.frame_index = 0
            
        self.image = animation[int(self.frame_index)]
        # Keep the rect aligned with the hitbox.
        self.rect = self.image.get_rect(midbottom=self.hitbox.midbottom)
    
    def get_player_distance_direction(self, player):
        # Calculates distance and normalized direction vector towards the player.
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2(0, 0)

        return (distance, direction)

    def get_status(self, player):
        # Determines the enemy's state based on distance to player.
        distance = self.get_player_distance_direction(player)[0]

        # If already attacking, stay in attack state until animation ends.
        if self.attacking:
            self.status = 'attack'
            return

        # Check if close enough to attack and cooldown is ready.
        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
        # Check if close enough to notice the player and chase.
        elif distance <= self.notice_radius:
            self.status = 'move'
        # Otherwise, stay idle.
        else:
            self.status = 'idle'

    def update(self):
        # Standard update method called by sprite groups.
        self.animate()
        self.cooldowns()
        self.check_death()
        
        # If in hit stun, we allow movement (knockback) regardless of status.
        # Otherwise, only move if status is 'move'.
        if self.hit_stun:
            self.move(self.speed)
        elif self.status == 'move':
            self.move(self.speed)

    def enemy_update(self, player):
        # AI logic update called specifically by the level class.
        self.get_status(player)
        self.actions()
        
        if self.hit_stun:
            # If stunned, set direction AWAY from the player (knockback).
            self.direction = -(self.get_player_distance_direction(player)[1])
        elif self.status == 'move':
            # If chasing, set direction TOWARD the player.
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            # Otherwise stop moving.
            self.direction = pygame.math.Vector2()
            
        self.update()