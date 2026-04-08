import pygame
from constants import *
from grid import make_grid, draw, get_clicked_pos
from algorithms import graph_colouring_bfs, hamiltonian_backtracking_dfs
from mazes import prims_maze

# Initialize Pygame and Fonts
pygame.init()
pygame.font.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DAA Pathfinding Visualizer — Premium Edition")

def main(win):
    ROWS = 39
    grid = make_grid(ROWS, GRID_WIDTH)

    start = None
    end = None

    run = True
    while run:
        draw(win, grid, ROWS, GRID_WIDTH)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # --- MOUSE INPUT ---
            if pygame.mouse.get_pressed()[0]: # LEFT CLICK
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, GRID_WIDTH)
                
                # Check if click was within grid
                if row is not None and col is not None:
                    node = grid[row][col]
                    
                    if not start and node != end:
                        start = node
                        start.make_start()
                    elif not end and node != start:
                        end = node
                        end.make_end()
                    elif node != end and node != start:
                        node.make_wall()

            elif pygame.mouse.get_pressed()[2]: # RIGHT CLICK
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, GRID_WIDTH)
                
                if row is not None and col is not None:
                    node = grid[row][col]
                    node.reset()
                    if node == start: start = None
                    elif node == end: end = None

            # --- KEYBOARD INPUT ---
            if event.type == pygame.KEYDOWN:
                # RUN BFS
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    graph_colouring_bfs(lambda: draw(win, grid, ROWS, GRID_WIDTH), grid, start, end)

                # RUN DFS (Hamiltonian Backtracking)
                if event.key == pygame.K_h and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    hamiltonian_backtracking_dfs(lambda: draw(win, grid, ROWS, GRID_WIDTH), grid, start, end)

                # GENERATE MAZE (Prim's Only)
                if event.key == pygame.K_g:
                    start, end = prims_maze(lambda: draw(win, grid, ROWS, GRID_WIDTH), grid, ROWS)

                # CLEAR GRID
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, GRID_WIDTH)

    pygame.quit()

if __name__ == "__main__":
    main(WIN)
