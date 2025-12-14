import pygame
from settings import *
from entity import Entity
from support import import_folder

class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacle_sprites, add_exp):
        # initialize base class and register with any provided groups
        super().__init__(*groups)
        self.sprite_type = 'enemy'

        self.import_graphics(monster_name)
        self.status = 'idle'

        # ensure we have at least one frame for the current status
        if self.animations.get(self.status) and len(self.animations[self.status]) > 0:
            self.image = self.animations[self.status][int(self.frame_index)]
        else:
            # fallback placeholder image when animation frames are missing
            self.image = pygame.Surface((64, 64), flags=pygame.SRCALPHA)
            self.image.fill((120, 20, 20))

        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
        # position vector for smooth movement
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.obstacle_sprites = obstacle_sprites

        # state for actions
        self.attacking = False
        self.can_attack = True
        self.attack_time = None
        # attack cooldown (ms) - default will be overridden by monster_data if present
        self.attack_cooldown = 1000

        self.monster_name = monster_name 
        monster_info = monster_data[self.monster_name] 
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_type']
        # per-monster cooldown override
        if 'attack_cooldown' in monster_info:
            self.attack_cooldown = monster_info['attack_cooldown']

        # Player interaction logic
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300
        
        # Hit stun logic
        self.hit_stun = False
        self.hit_stun_duration = 300
        
        # Function to grant EXP to player
        self.add_exp = add_exp
    
    def actions(self):
        # Prevent starting attacks if stunned
        if self.hit_stun:
            return

        # called when evaluating what the enemy should do this frame
        # Only start an attack if valid state, cooldown ready, and not currently attacking
        if self.status == 'attack' and self.can_attack and not self.attacking:
            print('attack')
            self.can_attack = False
            self.attack_time = pygame.time.get_ticks()
            self.attacking = True

    def get_damage(self, player, attack_type):
        if self.vulnerable:
            if attack_type == 'weapon':
                self.health -= player.get_full_weapon_damage()
            else:
                # Magic damage calculation based on player stats
                magic_damage = player.stats['magic'] + magic_data[player.magic]['strength']
                self.health -= magic_damage
            
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False
            
            # Apply Hit Stun
            self.hit_stun = True
            # Interrupt any current attack
            self.attacking = False

    def check_death(self):
        if self.health <= 0:
            self.add_exp(self.exp) # Grant EXP before death
            self.kill()

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        
        # handle resetting attack availability after cooldown
        if not self.can_attack and self.attack_time is not None:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
                self.attack_time = None
        
        # handle invincibility cooldown
        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

        # handle hit stun cooldown
        if self.hit_stun:
            if current_time - self.hit_time >= self.hit_stun_duration:
                self.hit_stun = False

    def import_graphics(self, name):
        self.animations = {'idle': [], 'move': [], 'attack': []}
        main_path = f'graphics/monsters/{name}/'
        for animation in self.animations.keys():
            full_path = main_path + animation
            self.animations[animation] = import_folder(main_path + animation)

    def animate(self):
        animation = self.animations[self.status]
        if not animation:
            return
            
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            # If the attack animation finished, unlock the state
            if self.status == 'attack':
                self.attacking = False
            self.frame_index = 0
            
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(midbottom=self.hitbox.midbottom)
    
    def get_player_distance_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2(0, 0)

        return (distance, direction)

    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]

        # 1. If currently attacking, lock status to 'attack' until animation finishes
        if self.attacking:
            self.status = 'attack'
            return

        # 2. Only transition to 'attack' if close enough AND cooldown is ready
        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'

    def update(self):
        # default update called by sprite groups: animate and move according to direction
        self.animate()
        self.cooldowns()
        self.check_death()
        
        # Allow movement if hit_stun is active (knockback) OR if status is move
        if self.hit_stun:
            # Move backwards (knockback) using normal speed
            self.move(self.speed)
        elif self.status == 'move':
            self.move(self.speed)

    def enemy_update(self, player):
        # high-level enemy logic called from camera group
        self.get_status(player)
        # run actions (attack once when appropriate)
        self.actions()
        
        if self.hit_stun:
            # Set direction AWAY from player for knockback
            self.direction = -(self.get_player_distance_direction(player)[1])
        elif self.status == 'move':
            # use direction toward player
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()
            
        # call the regular update (no args)
        self.update()