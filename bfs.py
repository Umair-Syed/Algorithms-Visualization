# Breadth First Search Algorithm Visualization
import sys
from utils import *
from pygame import time

# Setup Window
pygame.display.set_caption("BFS Algorithm")


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


# Backtracking 
def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.set_path()
        draw()


# draw is draw funtion, grid is 2d list of nodes
def algorithm(draw, grid, source, destination):
    count = 0
    open_set = []
    # put source node in queue
    open_set.append(source)
    # came_from dictionary for backtracking
    came_from = {}
    open_set_hash = {source}  # keeps track of what's in the open set

    while not len(open_set) == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # current = open_set.get()
        # open_set_hash.remove(current)
        current = open_set.pop(0)
        open_set_hash.remove(current)

        if current == destination:  # path FOUND!
            reconstruct_path(came_from, destination, draw)
            destination.set_destination()
            return True

        for neighbor in current.neighbors:
            if not neighbor.is_visited():        
                came_from[neighbor] = current
                if neighbor not in open_set_hash:
                        count += 1
                        open_set.append(neighbor)
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

    for i in range(rows + 1):
        # drawing horizontal line. (0, i*gap) is the start point and (width, i*gap) is the end point
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))

    for j in range(rows):
        # drawing vertical line. (j*gap, 0) is the start point and (j*gap, width) is the end point
        pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


# updates display with new draws
def draw(win, grid, rows, width, msg):
    # make everything white 
    win.fill(WHITE)

    # draw nodes
    for row in grid:
        for node in row:
            node.draw(win)

    # draw boundries
    draw_grid(win, rows, width)
    draw_text(msg, normal_font, ORANGE_RED, win, width//2, width + 20)
    # updates display
    pygame.display.update()
    time.wait(10)


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
    msg = 'Press SPACE to start'

    run = True
    while run:
        draw(win, grid, rows, width, msg)
        for event in pygame.event.get():  # contains all events
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if pygame.mouse.get_pressed(3)[0]:  # Left click
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

            elif pygame.mouse.get_pressed()[2]:  # Right click, remove node
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
                    msg = 'BFS Algorithm running...'
                    found = algorithm(lambda: draw(win, grid, rows, width, msg), grid, source, destination)
                    print("ALgorithm Finished")
                    if found:
                         msg = 'Path Found!'
                    else:
                         msg = 'No Path Found!'

                if event.key == pygame.K_c:  # reset
                    source = None
                    destination = None
                    grid = make_grid(rows, width)
                    msg = 'Press SPACE to start'

                if event.key == pygame.K_ESCAPE:
                    run = False
