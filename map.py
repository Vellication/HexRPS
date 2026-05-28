'''
A simulation of war represented with a 2-Paradox tournament.
Inspired by similar work done by Fractal Philosophy on YouTube.
'''

import math
import random

# Precomputed corner offsets for flat-top hexagons (unit size)
HEX_CORNER_OFFSETS = [
    (math.cos(math.radians(60 * i)), math.sin(math.radians(60 * i)))
    for i in range(6)
]

# Element Stuff

class Element:
    '''A single Element of the tournament (e.g. Fire). Contains its links'''
    def __init__(self, name):
        self.name = name
        self.beats = set()

    def compare(self, other):
        return other in self.beats

    def add_beats(self, beats):
        for beat in beats:
            if not isinstance(beat, Element) or beat.name == self.name:
                raise ValueError("Beats set incorrectly constructed")
        self.beats = set(beats)

# Map Stuff

class Hexagon:
    '''An individual hexagon, contains its coordinates and element'''
    def __init__(self, q, r, s, element=None):
        if q + r + s != 0:
            raise ValueError("Invalid coordinates")
        self.q = q
        self.r = r
        self.s = s
        self.element = element

    def getNeighbors(self):
        return (
            (self.q,     self.r + 1, self.s - 1),
            (self.q,     self.r - 1, self.s + 1),
            (self.q + 1, self.r,     self.s - 1),
            (self.q - 1, self.r,     self.s + 1),
            (self.q + 1, self.r - 1, self.s),
            (self.q - 1, self.r + 1, self.s),
        )

    def add_element(self, element):
        if isinstance(element, Element):
            self.element = element

class Map:
    '''A series of coordinates representing a hex map'''
    def __init__(self, size, elements):
        self.tiles = {}
        self.elements = elements if elements is not None else []
        for q in range(-size, size + 1):
            for r in range(-size, size + 1):
                s = -q - r
                if max(abs(q), abs(r), abs(s)) <= size:
                    self.tiles[(q, r, s)] = Hexagon(q, r, s)

    def get_hex(self, coords):
        return self.tiles.get(coords)

    def simulation_start_rand(self, elements):
        '''Pseudorandom starting conditions'''
        self.elements = elements
        if not all(isinstance(e, Element) for e in elements):
            raise TypeError("Elements set incorrectly constructed")
        element_counter = {e: 0 for e in elements}
        for tile in self.tiles.values():
            choice = random.choice(self.elements)
            element_average = sum(element_counter.values()) / len(self.elements)
            repeat_counter = 0
            while element_counter[choice] >= element_average * 1.2 and repeat_counter <= 5:
                choice = random.choice(self.elements)
                repeat_counter += 1
            element_counter[choice] += 1
            tile.add_element(choice)

    def simulation_next_step(self):
        '''Does RPS simultaneously, then adds some noise'''
        next_states = {}

        # First pass: compute next state for each tile
        for coords, tile in self.tiles.items():
            # Guard: skip tiles with no element
            if tile.element is None:
                next_states[coords] = random.choice(self.elements)
                continue

            neighbors = {}
            neighbor_count = 0
            for neighbor_coords in tile.getNeighbors():
                this_neighbor = self.get_hex(neighbor_coords)  # single lookup
                if this_neighbor is None or this_neighbor.element is None:
                    continue
                neighbor_count += 1
                if not tile.element.compare(this_neighbor.element):
                    neighbors[this_neighbor.element] = \
                        neighbors.get(this_neighbor.element, 0) + 1

            if neighbor_count > 0 and sum(neighbors.values()) >= neighbor_count / 2:
                beat_by = [e for e in neighbors if neighbors[e]]
                next_states[coords] = random.choice(beat_by)
            else:
                next_states[coords] = tile.element

        # Second pass: apply all changes
        for coords, element in next_states.items():
            self.tiles[coords].add_element(element)

        # Noise
        for tile in self.tiles.values():
            if random.random() < 0.000002:
                tile.add_element(random.choice(self.elements))


def flat_hex_to_pixel(hex, size, offset=(0, 0)):
    '''Finds the center of a hex; offset moves the grid on screen'''
    x = size * (3/2 * hex.q)
    y = size * (math.sqrt(3)/2 * hex.q + math.sqrt(3) * hex.r)
    return x + offset[0], y + offset[1]


def flat_hex_corners(cx, cy, size):
    '''Returns the 6 corner points of a flat-top hex given its center and size'''
    return [
        (cx + size * dx, cy + size * dy)
        for dx, dy in HEX_CORNER_OFFSETS
    ]