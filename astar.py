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
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Node:
    def __init__(self, row, col, width, totalRows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.totalRows = totalRows

    def getPosition(self):
        return self.row, self.col
    
    def isVisited(self):
        return self.color == RED

    def isCurrent(self):
        return self.color == GREEN

    def isBarrier(self):
        return self.color = BLACK
    
    def isSource(self):
        return self.color = ORANGE
    
    def isDestination(self):
        return self.color == TURQUOISE


    def resetNode(self):
        return self.color = WHITE

    def setVisited(self):
        self.color = RED
    
    def setCurrent(self):
        self.color = GREEN

    def setBarrier(self):
        self.color = BLACK

    def setDestination(self):
        self.color = TURQUOISE

    def setPath(self):
        self.color = PURPLE

    
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def updateNeighbors(self, grid):
        pass

    def __lt__(self, other):
        return False   

    
