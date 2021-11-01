import pygame


class Square:
    # static variables
    WIDTH = 100
    SIZE = (WIDTH, WIDTH)
    LIGHT_COLOR = (255, 253, 208)
    DARK_COLOR = (0, 102, 204)

    def __init__(self, color, location):
        self.color = color
        self.location = location

    def draw(self):
        pygame.draw.rect(pygame.display.get_surface(), self.color, pygame.Rect(self.location, self.SIZE))
