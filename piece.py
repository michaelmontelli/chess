import pygame


class Piece:
    WIDTH = 100
    SIZE = (WIDTH, WIDTH)

    def __init__(self, color, location):
        self.image = self._get_image(self.__class__.__name__.lower(), color)
        self.location = location

    def move(self):
        pass

    def draw(self):
        pygame.display.get_surface().blit(self.image, self.location)

    @staticmethod
    def _get_image(piece_type, color):
        piece_image = pygame.image.load(f"images/{piece_type}-{color}.svg")
        return pygame.transform.scale(piece_image, Piece.SIZE)

