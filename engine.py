import pygame
from pygame.locals import *
from board import Board


class Engine:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 800

    def __init__(self):
        self._running = False
        self._display_surface = None
        self.size = (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

    def initialize_engine(self):
        pygame.init()
        self._display_surface = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True

    # Process events
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    # Compute changes
    def on_loop(self):
        # pygame.draw.rect(pygame.display.get_surface(), pygame.Color(255, 255, 255), pygame.Rect(0, 0, 100, 100))
        board = Board()
        board.draw()

    # Print graphics on screen
    def render(self):
        pygame.display.flip()

    def cleanup(self):
        pygame.quit()

    def execute(self):
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.render()
        self.cleanup()


if __name__ == "__main__":
    engine = Engine()
    engine.initialize_engine()
    engine.execute()
