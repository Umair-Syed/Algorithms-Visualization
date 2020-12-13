# A* Shortest Path Algorithm Visualization
import pygame
from queue import PriorityQueue

# setting up window
pygame.display.set_caption("A* Shortest Path Algorithm")

# colors tuples
RED = (255, 0, 0)  # Visited
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)  # Destination
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)  # Not visited
BLACK = (0, 0, 0)  # Barrier
PURPLE = (128, 0, 128)  # Path
ORANGE = (255, 165, 0)  # Source
GREY = (128, 128, 128)  # Grid boundry
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

    def set_source(self):
        self.color = ORANGE

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
        self.neighbors = []

        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    # less than  (this < other) 
    def __lt__(self, other):
        return False

    # Heuristics function (using Manhattan Distance)


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x2 - x1) + abs(y2 - y1)


# Backtracking 
def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.set_path()
        draw()


# draw is draw funtion, grid is 2d list of nodes
def algorithm(draw, grid, source, destination):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count,
                  source))  # put source node in PQ. Priority a/c to f_score([0]), otherwise count [1] (ie which inserted first?)
    came_from = {}  # for backtracking
    g_score = {node: float("inf") for row in grid for node in row}  # current shortest distance from source to this node
    g_score[source] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[source] = h(source.get_position(), destination.get_position())

    open_set_hash = {source}  # keeps track whats in open_set

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]  # get node from priority queue (min f_score)
        open_set_hash.remove(current)

        if current == destination:  # path FOUND!
            reconstruct_path(came_from, destination, draw)
            destination.set_destination()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_position(), destination.get_position())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.set_current()

        draw()

        if current != destination:
            current.set_visited()

    return False


# param: rows_count = no of rows, width = width in pixels. Example (50, 800)
# returns 2d list of Nodes
def make_grid(rows_count, width):
    grid = []

    # gap is width or height of one box(node)
    gap = width // rows_count
    for i in range(rows_count):
        grid.append([])
        for j in range(rows_count):
            node = Node(i, j, gap, rows_count)
            grid[i].append(node)

    return grid


# draws grid boundries
def draw_grid(win, rows, width):
    gap = width // rows

    for i in range(rows):
        # drawing horizontal line. (0, i*gap) is the start point and (width, i*gap) is the end point
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))

    for j in range(rows):
        # drawing vertical line. (j*gap, 0) is the start point and (j*gap, width) is the end point
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


# param: pos = x y coordinates
# return: row and col of node clicked on 
def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def run_visualization(win, width):
    rows = 50
    grid = make_grid(rows, width)

    source = None
    destination = None

    run = True
    while run:
        draw(win, grid, rows, width)
        for event in pygame.event.get():  # contains all events
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # Left click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, width)
                node = grid[row][col]
                if not source and node != destination:
                    source = node
                    source.set_source()
                elif not destination and node != source:
                    destination = node
                    destination.set_destination()
                elif node != destination and node != source:
                    node.set_barrier()

            elif pygame.mouse.get_pressed()[2]:  # Right click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, width)
                node = grid[row][col]
                node.reset_node()
                if node == source:
                    source = None
                elif node == destination:
                    destination = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and source and destination:  # start
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    algorithm(lambda: draw(win, grid, rows, width), grid, source, destination)

                if event.key == pygame.K_BACKSPACE:  # reset
                    source = None
                    destination = None
                    grid = make_grid(rows, width)

    pygame.quit()

