import pygame


class Board:
    SCREEN_WIDTH = SCREEN_HEIGHT = 800

    def __init__(self):
        pygame.init()

        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


