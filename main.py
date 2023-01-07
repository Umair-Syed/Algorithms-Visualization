import astar
import bfs
import insertion_sort
import sys
from utils import *  # imports pygame
from pygame.locals import *

# Setup window
SCREEN_WIDTH = 550
SCREEN_HEIGHT = 630
pygame.display.set_caption("Algorithms Visualization")

_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
_click = False


def run_main():
    global _click
    while True:
        _screen.fill(DARK_SLATE_GRAY)

        draw_text('Algorithms Visualization', pygame.font.SysFont('Lato', 32, True),
                  ORANGE_RED, _screen, SCREEN_WIDTH // 2, 50)
        draw_text('Main Menu', normal_font, ORANGE_RED, _screen, SCREEN_WIDTH // 2, 120)

        underline_font = pygame.font.SysFont('Lato', 15)
        underline_font.set_underline(True)
        git_hub = draw_text('Project on GitHub', underline_font,
                            WHITE, _screen, 100, SCREEN_WIDTH - 20)

        mouse_pos = pygame.mouse.get_pos()
        # TODO: add calls here
        a_star_btn = normal_button((125, 180), (100, 30), _screen, 'A Star', mouse_pos)
        bfs_btn = normal_button((125, 230), (100, 30), _screen, 'BFS', mouse_pos)
        insertion_btn = normal_button((325, 180), (120, 30), _screen, 'Insertion Sort', mouse_pos)
        bubble_btn = normal_button((325, 230), (120, 30), _screen, 'Bubble Sort', mouse_pos)
        help_btn = normal_button((SCREEN_WIDTH - 120, SCREEN_WIDTH - 30), (100, 30), _screen, 'Help', mouse_pos, color=BLUE)
        if _click:
            set_click_listener(a_star_btn, mouse_pos, lambda: astar.run_visualization(_screen, SCREEN_WIDTH))
            set_click_listener(bfs_btn, mouse_pos, lambda: bfs.run_visualization(_screen, SCREEN_WIDTH))
            set_click_listener(insertion_btn, mouse_pos, lambda: insertion_sort.run_visualization(_screen, SCREEN_WIDTH))
            set_click_listener(git_hub, mouse_pos, lambda: webbrowser.open('https://github.com/Umair-Syed/Algorithms'
                                                                           '-Visualization.git', new=2))
            

        _click = False
        # _click = is_clicked()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    _click = True
    

        pygame.display.update()


run_main()
