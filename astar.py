import pygame
import math
from queue import PriorityQueue

# setting up window
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH)) 
pygame.display.set_caption("A* Shortest Path Algorithm")

# colors tuples
RED = (255, 0, 0)           # Visited
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)          # Destination
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)     # Not visited
BLACK = (0, 0, 0)           # Barrier
PURPLE = (128, 0, 128)      # Path
ORANGE = (255, 165 ,0)      # Source
GREY = (128, 128, 128)      # Grid boundry
TURQUOISE = (64, 224, 208)

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_position(self):
        return self.row, self.col
    
    def is_visited(self):
        return self.color == RED

    def is_current(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK
    
    def is_source(self):
        return self.color == ORANGE
    
    def is_destination(self):
        return self.color == TURQUOISE


    def reset_node(self):
        self.color = WHITE

    def set_visited(self):
        self.color = RED
    
    def set_current(self):
        self.color = GREEN

    def set_barrier(self):
        self.color = BLACK

    def set_destination(self):
        self.color = TURQUOISE

    def set_path(self):
        self.color = PURPLE

    
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        pass

    # less than  (this < other) 
    def __lt__(self, other): 
        return False   


# Heuristics function (using Manhattan Distance)
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x2 - x1) + abs(y2 - y1)


# will return 2d list of Nodes
def make_grid(rows_count, width):
    grid = []

    # gap is width/height of one box(node)
    gap = width // rows_count  
    for i in range(rows_count):
        grid.append([])
        for j in range(rows_count):
            node = Node(i, j, gap, rows_count)
            grid[i].append(node)
    
    return grid


# will draw grid boundries
def draw_grid(win, rows, width):
    gap = width // rows

    for i in range(rows):
        # drawing horizontal line (0, i*gap) is the start point and (width, i*gap) is the end point
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))

    for j in range(rows):
        # drawing vertical line (j*gap, 0) is the start point and (j*gap, width) is the end point
        pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


# updates display with new draws
def draw(win, grid, rows, width):
    # make everything white 
    win.fill(WHITE) 

    # draw nodes
    for row in grid:
        for node in row:
            node.draw(win)
            
    # draw boundries
    draw_grid(win, rows, width)

    # updates display
    pygame.display.update() 

