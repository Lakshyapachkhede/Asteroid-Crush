import pygame
import sys
from settings import *
from game import Game


pygame.init()



if __name__ == '__main__':
    game = Game()
    game.loop()

pygame.quit()
sys.exit()
