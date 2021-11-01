import pygame
import model
from eventmanager import *

WIDTH = HEIGHT = 800
DIMENSION = 8
SQUARE_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
WHITE = (255, 253, 208)
BLACK = (0, 102, 204)
IMAGES = {}


class GraphicalView:
    """
    Draw the model state onto the screen.
    """

    def __init__(self, event_manager, model):
        """
        :param event_manager: Allows posting messages to the event queue.
        :param model: a strong reference to the game Model.
        """

        self.event_manager = event_manager
        event_manager.register_listener(self)
        self.model = model
        self.is_initialized = False
        self.screen = None
        self.clock = None

    def notify(self, event):
        """
        Receive events posted to the message queue.
        """
        if isinstance(event, InitializeEvent):
            self.initialize()
        elif isinstance(event, QuitEvent):
            # shut down the pygame graphics
            self.is_initialized = False
            pygame.quit()
        elif isinstance(event, TickEvent):
            self.render_all()
            # limit the redraw speed to MAX_FPS frames per second
            self.clock.tick(MAX_FPS)

    def render_all(self):
        """
        Draw the current game state on screen.
        Does nothing if is_initialized == False (pygame.init failed).
        """

        if not self.is_initialized:
            return
        self.draw_board()
        # flip the display to show whatever we drew
        pygame.display.flip()

    def initialize(self):
        """
        Set up the physical graphical display and loads graphical resources.
        """

        result = pygame.init()
        pygame.display.set_caption('Chess')
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.is_initialized = True

    def draw_board(self):
        """Draws the squares on the board"""
        colors = [pygame.Color(WHITE), pygame.Color(BLACK)]
        for row in range(DIMENSION):
            for column in range(DIMENSION):
                color = colors[(row + column) % 2]  # Light squares have even parity, dark have odd parity
                pygame.draw.rect(self.screen,
                                 color,
                                 pygame.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                                 )

    def draw_pieces(self):
        """Draws the pieces on the board from the current game state."""
        for row in range(DIMENSION):
            for column in range(DIMENSION):
                piece = model.board[row, column]
                if piece != '-':
                    self.screen.blit(IMAGES[piece],
                                     pygame.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
