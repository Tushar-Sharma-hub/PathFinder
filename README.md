# Pathfinding Visualizer — Python DAA Project

This is a visualization tool designed to demonstrate various **Design & Analysis of Algorithms (DAA)** concepts in Python.

## Algorithms
- **Hamiltonian Cycle (Backtracking DFS)**: Explores all possible paths and visualizes the backtracking process.
- **Graph Colouring (BFS)**: Explores level by level, assigning "colors" (open set) to nodes.
- **Prim's Algorithm**: Generates complex mazes using Minimum Spanning Tree logic.

## Prerequisites
- Python 3.8+
- Pygame (`pip install pygame`)
- Streamlit (`pip install streamlit`)

## How to Run

### 1. Desktop Application (Pygame)
Provides high-performance animations and interactive grid controls.
```bash
python3 main.py
```
- **Left Click**: Place Start, then End, then Walls.
- **Right Click**: Reset Node.
- **SPACE**: Run Graph Colouring (BFS).
- **H**: Run Hamiltonian Backtracking (DFS).
- **G**: Generate Prim's Maze.
- **C**: Clear Grid.

### 2. Web Application (Streamlit)
A browser-based version with sidebar controls.
```bash
streamlit run app.py
```

## Implementation
The project is built entirely in Python, focusing on algorithmic clarity and visual performance for DAA evaluation.
