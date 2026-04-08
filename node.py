import pygame
from constants import *

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = col * width
        self.y = row * width
        self.color = NODE_DEFAULT
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        
        self.is_start = False
        self.is_end = False
        self.is_wall = False
        self.is_open = False
        self.is_closed = False
        self.is_path = False
        self.previous = None

    def get_pos(self):
        return self.row, self.col

    def reset(self):
        self.is_start = False
        self.is_end = False
        self.is_wall = False
        self.is_open = False
        self.is_closed = False
        self.is_path = False
        self.color = NODE_DEFAULT
        self.previous = None

    def make_start(self):
        if not self.is_wall:
            self.reset()
            self.is_start = True
            self.color = NODE_START

    def make_end(self):
        if not self.is_wall:
            self.reset()
            self.is_end = True
            self.color = NODE_END

    def make_wall(self):
        if not self.is_start and not self.is_end:
            self.reset()
            self.is_wall = True
            self.color = NODE_WALL

    def make_open(self):
        self.is_open = True
        if not self.is_start and not self.is_end:
            self.color = NODE_OPEN

    def make_closed(self):
        self.is_closed = True
        if not self.is_start and not self.is_end:
            self.color = NODE_CLOSED

    def make_path(self):
        self.is_path = True
        if not self.is_start and not self.is_end:
            self.color = NODE_PATH

    def draw(self, win):
        # Add a small padding for a better grid look
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        # Down
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_wall:
            self.neighbors.append(grid[self.row + 1][self.col])

        # Up
        if self.row > 0 and not grid[self.row - 1][self.col].is_wall:
            self.neighbors.append(grid[self.row - 1][self.col])

        # Right
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_wall:
            self.neighbors.append(grid[self.row][self.col + 1])

        # Left
        if self.col > 0 and not grid[self.row][self.col - 1].is_wall:
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False
