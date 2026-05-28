from map import *
import pygame

pygame.init()
SCREEN_X = 1400
SCREEN_Y = 1000
screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
HEX_SIZE = 6
DRAW_SIZE = HEX_SIZE * 0.93
last_step = 0
STEP_INTERVAL = 50  # milliseconds

fire      = Element("Fire")
water     = Element("Water")
wood      = Element("Wood")
earth     = Element("Earth")
metal     = Element("Metal")
void      = Element("Void")
lightning = Element("Lightning")

fire.add_beats({water, wood, void})
water.add_beats({wood, earth, metal})
wood.add_beats({void, metal, lightning})
earth.add_beats({fire, lightning, wood})
metal.add_beats({void, earth, fire})
void.add_beats({lightning, water, earth})
lightning.add_beats({fire, water, metal})

COLORS = {
    fire:      (255, 0,   0),
    water:     (0,   0,   255),
    wood:      (125, 91,  15),
    earth:     (0,   255, 0),
    metal:     (139, 149, 156),
    void:      (219, 0,   255),
    lightning: (255, 255, 0),
}

def darken(color, factor):
    return tuple(int(value * (1 - factor)) for value in color)

# Precompute dark colors so darken() isn't called every frame
DARK_COLORS = {e: darken(COLORS[e], 0.5) for e in COLORS}

elements = [fire, water, wood, earth, metal, void, lightning]

class ScreenMap(Map):
    def __init__(self, hex_size, elements):
        self.tiles = {}
        self.elements = elements if elements is not None else []
        q_range = int(SCREEN_X / (hex_size * 3/2)) + 2
        r_range = int(SCREEN_Y / (hex_size * math.sqrt(3))) + 2
        for q in range(-q_range, q_range + 1):
            for r in range(-r_range, r_range + 1):
                s = -q - r
                cx, cy = flat_hex_to_pixel(
                    type('H', (), {'q': q, 'r': r})(),
                    hex_size,
                    (SCREEN_X/2, SCREEN_Y/2)
                )
                if 0 <= cx <= SCREEN_X and 0 <= cy <= SCREEN_Y:
                    self.tiles[(q, r, s)] = Hexagon(q, r, s)

hex_map = ScreenMap(HEX_SIZE, elements)

# Start all tiles as fire
for tile in hex_map.tiles.values():
    tile.add_element(fire)

# Precompute pixel centers — map never moves so no need to recalculate each frame
OFFSET = (SCREEN_X / 2, SCREEN_Y / 2)
pixel_centers = {
    coords: flat_hex_to_pixel(tile, HEX_SIZE, OFFSET)
    for coords, tile in hex_map.tiles.items()
}

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    now = pygame.time.get_ticks()
    if now - last_step >= STEP_INTERVAL:
        hex_map.simulation_next_step()
        last_step = now

    screen.fill((0, 0, 0))
    for coords, tile in hex_map.tiles.items():
        cx, cy = pixel_centers[coords]
        corners = flat_hex_corners(cx, cy, DRAW_SIZE)
        color = COLORS[tile.element]
        dark  = DARK_COLORS[tile.element]
        pygame.draw.polygon(screen, dark,  corners)
        pygame.draw.polygon(screen, color, corners, 2)

    pygame.display.flip()