import pygame
from node import Node
from constants import *

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows + 1):
        pygame.draw.line(win, GRID_COLOR, (0, i * gap), (width, i * gap))
        pygame.draw.line(win, GRID_COLOR, (i * gap, 0), (i * gap, width))

def draw_ui(win):
    # Draw side panel
    pygame.draw.rect(win, UI_BG_COLOR, (GRID_WIDTH, 0, PANEL_WIDTH, HEIGHT))
    
    # Title
    font = pygame.font.SysFont('Arial', 24, bold=True)
    title = font.render("Pathfinder DAA", True, TEXT_COLOR)
    win.blit(title, (GRID_WIDTH + 20, 30))
    
    # Instructions
    info_font = pygame.font.SysFont('Arial', 16)
    instructions = [
        "CONTROLS:",
        "L-Click: Set Start/End/Walls",
        "R-Click: Clear Node",
        "SPACE: Run BFS",
        "H: Run Hamiltonian Backtracking",
        "G: Generate Prim's Maze",
        "C: Clear Grid",
        "",
        "LEGEND:",
        "Green: Start",
        "Red: End",
        "Yellow: Path",
        "Blue: Explored"
    ]
    
    for i, line in enumerate(instructions):
        text = info_font.render(line, True, TEXT_COLOR)
        win.blit(text, (GRID_WIDTH + 20, 80 + i * 25))

def draw(win, grid, rows, width):
    win.fill(BG_COLOR)

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, width)
    draw_ui(win)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    if x >= width or y >= width:
        return None, None

    row = y // gap
    col = x // gap
    
    # Double check bounds
    row = max(0, min(row, rows - 1))
    col = max(0, min(col, rows - 1))

    return row, col
