import pygame
from collections import deque

def reconstruct_path(came_from, current, draw):
    """Visualizes the final path back to start."""
    path = []
    while current in came_from:
        current = came_from[current]
        if not current.is_start:
            current.make_path()
            path.append(current)
            draw()
            # Add a slight delay for path animation
            pygame.time.delay(10)
    return path

def graph_colouring_bfs(draw, grid, start, end):
    """
    Graph Colouring BFS: Level-by-level exploration.
    """
    if not start or not end: return False
    
    queue = deque([start])
    came_from = {}
    visited = {start}

    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        current = queue.popleft()

        if current == end:
            reconstruct_path(came_from, end, draw)
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                neighbor.make_open()
                queue.append(neighbor)
        
        draw()
        if current != start:
            current.make_closed()

    return False

def hamiltonian_backtracking_dfs(draw, grid, start, end):
    """
    Hamiltonian Backtracking DFS: Deep path exploration.
    """
    if not start or not end: return False
    
    # We'll use a stack for DFS
    stack = [start]
    came_from = {}
    visited = {start}

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        current = stack.pop()

        if current == end:
            reconstruct_path(came_from, end, draw)
            return True

        if current != start:
            current.make_closed()

        # Get neighbors and Reverse to maintain consistent direction
        for neighbor in reversed(current.neighbors):
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                neighbor.make_open()
                stack.append(neighbor)
        
        draw()

    return False
