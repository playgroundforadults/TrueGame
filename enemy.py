import pygame
from settings import *
from entity import Entity
from support import import_folder

class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacle_sprites):
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

        self.monster_name = monster_name 
        monster_info = monster_data[self.monster_name] 
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_type']
    
        self.can_attack = True
    
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

        if distance <= self.attack_radius and not self.attacking:
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'

    def update(self):
        # default update called by sprite groups: animate and move according to direction
        self.animate()
        if self.status == 'move':
            self.move(self.speed)

    def enemy_update(self, player):
        # high-level enemy logic called from camera group
        self.get_status(player)
        # set movement direction when noticing player
        if self.status == 'move':
            # use direction toward player
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()
        # call the regular update (no args)
        self.update()