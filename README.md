# Pacman Search Algorithms AI

AI course project focused on solving a Pacman pathfinding problem using uninformed and informed search algorithms.

## Overview

Pacman must collect all fruits in a maze while avoiding walls and moving ghosts.

The objective is to find a valid path with the minimum number of moves. In this problem, Pacman must first collect all fruits of type `A` and then collect fruits of type `B`.

## Implemented Algorithms

- Breadth-First Search (BFS)
- Depth-First Search (DFS)
- Iterative Deepening Search (IDS)
- A* Search
- Weighted A* Search

## Features

- Pacman maze environment
- Moving ghost simulation
- Fruit collection constraints
- Search-based pathfinding
- Heuristic-based optimization
- Weighted A* comparison
- Map-based testing
- Pygame visualization

## Technologies

- Python
- Artificial Intelligence
- Search Algorithms
- Pathfinding
- Pygame

## Project Structure

```text
.
├── assets/       # Game assets
├── core/         # Game environment and search logic
├── entities/     # Game entities
├── maps/         # Test maps
├── config.py
├── main.py
├── menu.py
├── run_local.py
└── tester.py
```

## How to Run

Install dependencies:

```bash
pip install pygame
```

Run the game:

```bash
python main.py
```

Run tests:

```bash
python tester.py
```

## Academic Context

This project was developed as part of an Artificial Intelligence course assignment.

The assignment required implementing BFS, DFS, IDS, A*, and Weighted A* to solve a Pacman search problem and compare their performance across different maps.

## Notes

This repository is organized for portfolio presentation and academic documentation.
