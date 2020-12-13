import pygame
import webbrowser

pygame.init()

# colors tuples
RED = (255, 0, 0)  # Visited
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)  # Destination
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)  # Not visited
BLACK = (0, 0, 0)  # Barrier
PURPLE = (128, 0, 128)  # Path
ORANGE = (255, 165, 0)  # Source
GREY = (128, 128, 128)  # Grid boundary
TURQUOISE = (64, 224, 208)
CRIMSON = (220, 20, 60)
ORANGE_RED = (255, 69, 0)
DARK_SLATE_GRAY = (47, 79, 79)

normal_font = pygame.font.SysFont('Lato', 25)
small_font = pygame.font.SysFont('lato', 15)


def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)
    return text_rect


# top_left = (left, top), dim = (width, height)
def normal_button(top_left, dim, screen, text, cursor_pos, color=ORANGE_RED, hover_color=RED, TEXT_COLOR=WHITE):
    button = pygame.Rect(top_left, dim)
    pygame.draw.rect(screen, color, button, border_radius=10)
    if button.collidepoint(cursor_pos):
        pygame.draw.rect(screen, hover_color, button, border_radius=10)

    # draw text in centre of button
    draw_text(text, small_font, TEXT_COLOR, screen, top_left[0] + (dim[0] // 2), top_left[1] + (dim[1] // 2))
    return button


def set_click_listener(rect, click_pos, on_click):
    if rect.collidepoint(click_pos):
        on_click()
