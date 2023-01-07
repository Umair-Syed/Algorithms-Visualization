# Insertion Sort Algorithm Visualization
import sys
from utils import *
from pygame import time
import random
from pygame.locals import *

# Setup Window
pygame.display.set_caption("Insertion Sort Algorithm")


start = False
list = []


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.width = width
        self.total_rows = total_rows

    def get_position(self):
        return self.row, self.col

    def reset_node(self):
        self.color = WHITE

    def set_cell(self):
        self.color = RED

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))


# draw is draw funtion,
def algorithm(draw,grid, make_bars,rows):
    for i in range(len(list)):
        for j in range(0,len(list)-i-1):
            if list[j]>list[j+1]:
                list[j],list[j+1] = list[j+1],list[j]
            make_bars(grid,rows)
            draw()
            time.wait(300)
        
        

def make_bars(grid,rows):
    left=1
    for i in range(len(list)):
        left=left+2
        j=rows-1
        while j>=rows-list[i]:
            grid[left][j].set_cell()
            j=j-1
        while j>0:
            grid[left][j].reset_node()
            j=j-1
       

# param: rows_count = no of rows, width = width in pixels. Example (50, 800)
# returns 1d list of Nodes
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
def draw(win, grid, rows, width, msg, _click):
    # make everything white 
    win.fill(WHITE)

    # draw nodes
    for row in grid:
        for node in row:
            node.draw(win)

    # draw boundries
    draw_grid(win, rows, width)
    draw_text(msg, normal_font, ORANGE_RED, win, width//2, width + 30)
    pos = pygame.mouse.get_pos()
    shuffle_btn = normal_button((int(width/1.35), width + 15), (110, 30), win, 'Shuffle', pos)
    sort_btn = normal_button((int(width/5.0), width + 15), (110, 30), win, 'Sort', pos)

    if _click:
        set_click_listener(shuffle_btn, pos, generate)
        set_click_listener(sort_btn, pos, start_func)
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
    rows = 25
    grid = make_grid(rows, width)
    
    generate()
    msg = ''
    make_bars(grid,rows)
    _click = False
    run = True

    global start
    start = False
    while run:
        draw(win, grid, rows, width, msg, _click)
        make_bars(grid,rows)
        if(start):
            algorithm(lambda: draw(win, grid, rows, width, msg, _click),grid,make_bars ,rows)
            start = False
        for event in pygame.event.get():  # contains all events
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            _click = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:  # reset                
                    grid = make_grid(rows, width)
                    msg = 'Press SPACE to start'

                if event.key == pygame.K_ESCAPE:
                    run = False

            if event.type == pygame.MOUSEBUTTONDOWN:  # Left click
                _click = True


def generate():
    list.clear()
    list.extend(random.sample(range(1, 11), 10))

def start_func():
    global start
    start = True

