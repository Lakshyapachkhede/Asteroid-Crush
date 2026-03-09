import pygame

pygame.init()
info = pygame.display.Info()

WINDOW_WIDTH = info.current_w
WINDOW_HEIGHT = info.current_h


GAME_NAME = "Asteroid Crush"
DEVELOPER = "Lakshya Pachkhede"
VERSION = "0.1"

GAME_STATE_MENU = 0
GAME_STATE_OVER = 1
GAME_STATE_LOOP = 2
GAME_STATE_CONTROLS = 3

CELL_W = 120
CELL_H = 120


RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
