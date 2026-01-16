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
        # Gets the display surface.
        self.display_surface = pygame.display.get_surface()

        # Initializes sprite groups.
        # YSortCameraGroup handles drawing sprites sorted by Y-coordinate for depth.
        self.visible_sprites = YSortCameraGroup()
        # Obstacles stop movement.
        self.obstacle_sprites = pygame.sprite.Group()
        # Attackable sprites include enemies and breakable grass.
        self.attackable_sprites = pygame.sprite.Group()
        # Attack sprites are weapons and magic projectiles created by the player.
        self.attack_sprites = pygame.sprite.Group()

        self.current_attack = None

        # Parses map data and spawns sprites.
        self.create_map()

        # Initializes the UI overlay.
        self.ui = UI()
        
        # Initializes magic and particle systems.
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

    
    def create_map(self):
        # Dictionary linking map layer names to CSV file paths.
        layouts = {
            'boundary': import_csv_layout('map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('map/map_Grass.csv'),
            'object': import_csv_layout('map/map_Objects.csv'),
            'entities': import_csv_layout('map/map_Entities.csv')
        }
        # Dictionary loading graphics for specific layers.
        graphics = {
            'grass': import_folder('graphics/Grass'),
            'object': import_folder('graphics/Objects')
        }
        
        # Iterates over each layout and tile to place sprites.
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * tile_size
                        y = row_index * tile_size
                        
                        # Invisible boundaries for collision.
                        if style == 'boundary':
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'invisible')
                        
                        # Grass tiles (now destructible).
                        if style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile(
                                (x, y), 
                                [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites], 
                                'grass', 
                                random_grass_image)
                        
                        # Object tiles (trees, rocks, etc.).
                        if style == 'object':
                            object_image = graphics['object'][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', object_image)
                        
                        # Entities (Player and Enemies).
                        if style == 'entities':
                            if col.strip() == '394':
                                self.player = Player(
                                    (x, y), 
                                    [self.visible_sprites], 
                                    self.obstacle_sprites, 
                                    self.create_attack, 
                                    self.destroy_attack, 
                                    self.create_magic)
                            else:
                                # Determine monster type based on ID.
                                if col.strip() == '390': monster_name = 'bamboo'
                                elif col.strip() == '391': monster_name = 'spirit'
                                elif col.strip() == '392': monster_name = 'raccoon'
                                else: monster_name = 'squid'
                                
                                Enemy(monster_name, (x, y), [self.visible_sprites, self.attackable_sprites], self.obstacle_sprites, self.add_exp)

    def create_attack(self):
        # creates a Weapon sprite and adds it to visible and attack groups.
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def create_magic(self, style, strength, cost):
        # Triggers magic spells via the magic_player.
        if style == 'heal':
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])
        
        if style == 'flame':
            self.magic_player.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])

    def destroy_attack(self):
        # Removes the weapon sprite when the attack animation ends.
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def add_exp(self, amount):
        # Callback to add EXP to the player.
        self.player.exp += amount

    def player_attack_logic(self):
        # Checks collisions between player's attacks and attackable sprites.
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            # Logic for destroying grass: spawn leaf particles and kill sprite.
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0, 75)
                            for _ in range(randint(3, 6)):
                                # Pick a random leaf particle type.
                                self.animation_player.create_particles(f'leaf{randint(1, 6)}', pos - offset, [self.visible_sprites])
                            target_sprite.kill()
                        else:
                            # Logic for damaging enemies.
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def damage_player(self):
        # Checks collisions between the player and enemies.
        if self.attackable_sprites:
            # Filter the list to only check collision with enemies, not grass.
            enemies = [sprite for sprite in self.attackable_sprites if sprite.sprite_type == 'enemy']
            collision_sprites = pygame.sprite.spritecollide(self.player, enemies, False)
            
            if collision_sprites:
                for enemy in collision_sprites:
                    # Logic runs only if the player is currently vulnerable (not in i-frames).
                    if self.player.vulnerable:
                        self.player.get_damage(enemy.attack_damage)
                        # Triggers the 'leaf_attack' hit effect exactly once per hit.
                        self.animation_player.create_particles('leaf_attack', self.player.rect.center, [self.visible_sprites])

    def run(self):
        # Updates all visible sprites.
        self.visible_sprites.update()
        
        # custom_draw handles the camera offset and depth sorting.
        self.visible_sprites.custom_draw(self.player)
        
        # Updates enemy AI logic.
        self.visible_sprites.enemy_update(self.player)
        
        # Handles combat collisions.
        self.player_attack_logic()
        self.damage_player()
        
        # Draws the UI elements.
        self.ui.display(self.player)
        
        # Checks if all enemies are defeated to display the victory message.
        enemies_left = [s for s in self.attackable_sprites if s.sprite_type == 'enemy']
        if len(enemies_left) == 0:
            self.ui.display_victory_message()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        # Initializes the custom sprite group.
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        
        # Calculates the center of the screen to keep the player centered.
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # Loads the background floor image.
        self.floor_surface = pygame.image.load("graphics/tilemap/ground.png").convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))


    def custom_draw(self, player):
        # updates the camera offset based on the player's position.
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        
        # Key function for sorting sprites by their Y-coordinate (creates pseudo-3D overlap).
        def sort_key(sprite):
            if hasattr(sprite, 'hitbox'):
                return sprite.hitbox.centery
            return sprite.rect.centery
        
        # Draws the floor first, offset by the camera position.
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)

        # Draws all sprites, sorted by their Y position.
        for sprite in sorted(self.sprites(), key=sort_key):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        # Calls the AI update method for all Enemy sprites in this group.
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)