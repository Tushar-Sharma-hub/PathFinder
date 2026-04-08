import random
import pygame

def prims_maze(draw, grid, rows):
    """
    Prim's Algorithm for Maze Generation as per DAA syllabus.
    Highly optimized for visual performance.
    """
    # 1. Fill grid with walls and clear start/end
    for row in grid:
        for node in row:
            node.reset()
            node.make_wall()
    
    draw()

    # Define nodes as odd coordinates to ensure boundaries work
    nodes = []
    for r in range(1, rows, 2):
        for c in range(1, rows, 2):
            nodes.append((r, c))

    if not nodes: return False
    
    # Pick a random starting point from our node list
    start_row, start_col = nodes[random.randint(0, len(nodes) - 1)]
    grid[start_row][start_col].reset()
    
    visited = {(start_row, start_col)}
    frontier = []
    
    # Add initial frontier cells
    def add_frontier(r, c):
        for dr, dc in [(0, 2), (0, -2), (2, 0), (-2, 0)]:
            nr, nc = r + dr, c + dc
            if 1 <= nr < rows - 1 and 1 <= nc < rows - 1:
                if (nr, nc) not in visited:
                    frontier.append((nr, nc, r, c)) # (new_node_r, new_node_c, from_node_r, from_node_c)

    add_frontier(start_row, start_col)
    
    while frontier:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        # Randomly select from frontier
        idx = random.randint(0, len(frontier) - 1)
        nr, nc, fr, fc = frontier.pop(idx)
        
        if (nr, nc) not in visited:
            visited.add((nr, nc))
            
            # Break the wall between from_node and new_node
            wr, wc = (nr + fr) // 2, (nc + fc) // 2
            grid[nr][nc].reset()
            grid[wr][wc].reset()
            
            add_frontier(nr, nc)
            draw()

    # Place Start and End nodes after maze is generated
    # Pick two distant points from the visited set
    visited_list = list(visited)
    if len(visited_list) >= 2:
        start_pos = visited_list[0]
        end_pos = visited_list[-1]
        
        start_node = grid[start_pos[0]][start_pos[1]]
        end_node = grid[end_pos[0]][end_pos[1]]
        
        start_node.make_start()
        end_node.make_end()
        
        return start_node, end_node

    return None, None
