# Sets the width of the game window in pixels.
width = 1280
# Sets the height of the game window in pixels.
height = 720
# Defines the target frames per second for the game loop.
fps = 60
# Defines the standard size (width and height) of a single tile in the grid.
tile_size = 64

# Sets the height for UI bars (health and energy).
bar_height = 20
# Sets the width of the player's health bar.
health_bar_width = 200
# Sets the width of the player's energy/magic bar.
magic_bar_width = 140
# Sets the size of the square box used to display items/weapons in the UI.
item_box_size = 80
# Specifies the file path to the font used for UI text.
ui_font = 'graphics/font/joystix.ttf'
# Sets the font size for UI text.
ui_font_size = 18

# Defines the color used for water elements (hex code).
water_color = '#71ddee'
# Defines the background color for UI elements.
ui_bg_color = '#222222'
# Defines the color for UI borders.
ui_border_color = '#111111'
# Defines the color for standard text.
text_color = '#eeeeee'

# Defines the color of the health bar.
health_color = 'red'
# Defines the color of the energy bar.
energy_color = 'blue'
# Defines the border color for the currently selected item in the UI.
ui_border_color_active = 'gold'

# A dictionary containing configuration data for different weapons.
# Keys are weapon names, values are dictionaries with cooldown, damage, and graphics path.
weapons_data = {
    'sword': {'cooldown': 400, 'damage': 5, 'graphic': 'graphics/weapons/sword/full.png'},
    'axe': {'cooldown': 600, 'damage': 10, 'graphic': 'graphics/weapons/axe/full.png'}
}

# A dictionary containing configuration data for magic spells.
# Keys are spell names, values are dictionaries with strength, energy cost, and graphics path.
magic_data = {
    'flame': {'strength': 5, 'cost': 20, 'graphic': 'graphics/particles/flame/fire.png'},
    'heal': {'strength': 20, 'cost': 10, 'graphic': 'graphics/particles/heal/heal.png'}
}

# A dictionary containing stats and attributes for different enemy types.
# Includes health, experience reward, movement speed, damage, attack/notice radius, attack type, and cooldown.
monster_data = {
    'bamboo': {
        'health': 50,
        'exp': 50,
        'speed': 2,
        'damage': 10,
        'attack_radius': 30,
        'notice_radius': 150,
        'attack_type': 'melee',
        'attack_cooldown': 1200
    },
    'spirit': {
        'health': 80,
        'exp': 80,
        'speed': 3,
        'damage': 12,
        'attack_radius': 40,
        'notice_radius': 200,
        'attack_type': 'ranged',
        'attack_cooldown': 900
    },
    'raccoon': {
        'health': 70,
        'exp': 70,
        'speed': 3,
        'damage': 14,
        'attack_radius': 35,
        'notice_radius': 160,
        'attack_type': 'melee',
        'attack_cooldown': 1000
    },
    'squid': {
        'health': 90,
        'exp': 90,
        'speed': 2,
        'damage': 18,
        'attack_radius': 45,
        'notice_radius': 180,
        'attack_type': 'ranged',
        'attack_cooldown': 1400
    }
}