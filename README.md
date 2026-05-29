# HexRPS

A cellular automaton simulation of elemental warfare on a hex grid, built in Python with pygame.

Inspired by [Fractal Philosophy](https://www.youtube.com/@FractalPhilosophy) on YouTube.

## Concept

Each hex tile is assigned one of seven elements. Each simulation step, a tile is converted to a neighboring element if it loses to a majority of its neighbors. The result is an emergent, ever-shifting territorial battle with no guaranteed winner.

The win/loss relationships form a **2-paradoxical tournament** — a directed graph where for any two elements, there exists a third that beats both. This ensures no element can dominate permanently.

## Elements & Relationships

The seven elements follow a cyclic pattern: each element beats the elements at positions +1, +2, and +4 in the cycle, and loses to the elements at positions +3, +5, and +6.

**Cycle:** Fire → Water → Wood → Earth → Metal → Void → Lightning

## Features

- Flat-top hex grid using cube coordinates (q, r, s)
- Simultaneous tile resolution
- Pseudorandom balanced starting conditions
- Low-rate noise to allow extinct elements to re-emerge
- Precomputed pixel centers and corner offsets for rendering performance

## Requirements

```
pygame
```

Install with:

```bash
pip install pygame
```

## Usage

```bash
python testMap1.py
```

## Project Structure

- `map.py` — core library: `Element`, `Hexagon`, `Map`, `ScreenMap`, and rendering utilities
- `testMap1.py` — pygame visualizer

## References

- [Hexagonal Grids — Red Blob Games](https://www.redblobgames.com/grids/hexagons/)
- [Tournament (graph theory) — Wikipedia](https://en.wikipedia.org/wiki/Tournament_(graph_theory))
