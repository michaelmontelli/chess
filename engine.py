import pygame
from pygame.locals import *
from board import Board
from pieces import (Pawn, Knight,
                    Bishop, Rook,
                    Queen, King)
from setup import Setup


class Engine:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 800

    def __init__(self):
        self.__is_running = False
        self.__display_surface = None
        self.size = (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

    def initialize_engine(self):
        pygame.init()
        self.__display_surface = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.__is_running = True

    # Process events
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.__is_running = False

    # Compute changes
    def on_loop(self):
        # pygame.draw.rect(pygame.display.get_surface(), pygame.Color(255, 255, 255), pygame.Rect(0, 0, 100, 100))
        board = Board()
        board.draw()
        # white_pawn = Pawn("white", (100, 100))
        # white_pawn.draw()
        # black_knight = King(King.BLACK, (200, 100))
        # black_knight.draw()
        Setup.setup_white_pawns()
        Setup.setup_black_pawns()
        # TODO: Instead of blitting pieces individually, find way to blit at the same time

    # Print graphics on screen
    def render(self):
        pygame.display.flip()


    def cleanup(self):
        pygame.quit()

    def execute(self):
        while self.__is_running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.render()
        self.cleanup()


if __name__ == "__main__":
    engine = Engine()
    engine.initialize_engine()
    engine.execute()
