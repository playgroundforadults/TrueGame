
width = 1280
height = 720
fps = 60
tile_size = 64

bar_height = 20
health_bar_width = 200
magic_bar_width = 140
item_box_size = 80
ui_font = 'graphics/font/joystix.ttf'
ui_font_size = 18

water_color = '#71ddee'
ui_bg_color = '#222222'
ui_border_color = '#111111'
text_color = '#eeeeee'

health_color = 'red'
energy_color = 'blue'
ui_border_color_active = 'gold'


weapons_data = {
    'sword': {'cooldown': 400, 'damage': 15, 'graphic': 'graphics/weapons/sword/full.png'},
    'axe': {'cooldown': 600, 'damage': 25, 'graphic': 'graphics/weapons/axe/full.png'}
}
magic_data = {
    'flame': {'strength': 5, 'cost': 20, 'graphic': 'graphics/particles/flame/fire.png'},
    'heal': {'strength': 20, 'cost': 10, 'graphic': 'graphics/particles/heal/heal.png'}
}

# Monster configuration used by Enemy
monster_data = {
    'bamboo': {
        'health': 50,
        'exp': 50,
        'speed': 2,
        'damage': 10,
        'attack_radius': 30,
        'notice_radius': 150,
        'attack_type': 'melee'
    },
    'spirit': {
        'health': 80,
        'exp': 80,
        'speed': 3,
        'damage': 12,
        'attack_radius': 40,
        'notice_radius': 200,
        'attack_type': 'ranged'
    },
    'raccoon': {
        'health': 70,
        'exp': 70,
        'speed': 3,
        'damage': 14,
        'attack_radius': 35,
        'notice_radius': 160,
        'attack_type': 'melee'
    },
    'squid': {
        'health': 90,
        'exp': 90,
        'speed': 2,
        'damage': 18,
        'attack_radius': 45,
        'notice_radius': 180,
        'attack_type': 'ranged'
    }
}