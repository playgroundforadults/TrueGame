import pygame
from settings import *

from tile import Tile
from player import Player
from support import *
from random import choice, randint
from weapon import Weapon
from ui import UI
from enemy import Enemy
from magic import MagicPlayer, AnimationPlayer

class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        # Groups
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group() # Enemies and Grass
        self.attack_sprites = pygame.sprite.Group()     # Weapon + Magic projectiles

        self.current_attack = None

        self.create_map()

        self.ui = UI()
        
        # Magic
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

    
    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('map/map_Grass.csv'),
            'object': import_csv_layout('map/map_Objects.csv'),
            'entities': import_csv_layout('map/map_Entities.csv')
        }
        graphics = {
            'grass': import_folder('graphics/Grass'),
            'object': import_folder('graphics/Objects')
        }
        
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    x = col_index * tile_size
                    y = row_index * tile_size
                    if style == 'boundary' and col != '-1':
                        Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'invisible')
                    if style == 'grass' and col != '-1':
                        random_grass_image = choice(graphics['grass'])
                        # Grass is now added to attackable_sprites
                        Tile(
                            (x, y), 
                            [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites], 
                            'grass', 
                            random_grass_image)
                    if style == 'object' and col != '-1':
                        object_image = graphics['object'][int(col)]
                        Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', object_image)
                    if style == 'entities' and col != '-1':
                        if col.strip() == '394':
                            self.player = Player(
                                (x, y), 
                                [self.visible_sprites], 
                                self.obstacle_sprites, 
                                self.create_attack, 
                                self.destroy_attack, 
                                self.create_magic)
                        else:
                            if col.strip() == '390': monster_name = 'bamboo'
                            elif col.strip() == '391': monster_name = 'spirit'
                            elif col.strip() == '392': monster_name = 'raccoon'
                            else: monster_name = 'squid'
                            
                            Enemy(monster_name, (x, y), [self.visible_sprites, self.attackable_sprites], self.obstacle_sprites, self.add_exp)

    def create_attack(self):
        # Pass attack_sprites to weapon so it can register itself for collision
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def create_magic(self, style, strength, cost):
        if style == 'heal':
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])
        
        if style == 'flame':
            self.magic_player.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def add_exp(self, amount):
        self.player.exp += amount

    def player_attack_logic(self):
        # Cycle through all active attack sprites (Weapon or Magic)
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0, 75)
                            # Spawn random leaf particles (leaf1 to leaf6)
                            for _ in range(randint(3, 6)):
                                self.animation_player.create_particles(f'leaf{randint(1, 6)}', pos - offset, [self.visible_sprites])
                            target_sprite.kill()
                        else:
                            # Enemy damage logic
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def damage_player(self):
        # Check collision between player and attackable sprites
        if self.attackable_sprites:
            # Filter enemies (ignore grass so walking on it doesn't hurt)
            enemies = [sprite for sprite in self.attackable_sprites if sprite.sprite_type == 'enemy']
            collision_sprites = pygame.sprite.spritecollide(self.player, enemies, False)
            
            if collision_sprites:
                for enemy in collision_sprites:
                    # Only play animation and take damage if player is vulnerable
                    if self.player.vulnerable:
                        self.player.get_damage(enemy.attack_damage)
                        # Play the 'leaf_attack' animation when player gets hit
                        self.animation_player.create_particles('leaf_attack', self.player.rect.center, [self.visible_sprites])

    def run(self):
        self.visible_sprites.update()
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.enemy_update(self.player)
        
        self.player_attack_logic()
        self.damage_player()
        
        self.ui.display(self.player)
        
        # Check for victory condition: No more enemies in the attackable group
        enemies_left = [s for s in self.attackable_sprites if s.sprite_type == 'enemy']
        if len(enemies_left) == 0:
            self.ui.display_victory_message()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        self.floor_surface = pygame.image.load("graphics/tilemap/ground.png").convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))


    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        
        def sort_key(sprite):
            if hasattr(sprite, 'hitbox'):
                return sprite.hitbox.centery
            return sprite.rect.centery
        
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=sort_key):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)