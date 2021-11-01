import pygame
import model
from eventmanager import *

WIDTH = HEIGHT = 800
DIMENSION = 8
SQUARE_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = [{}, {}]

ColorType = bool
COLORS = [WHITE, BLACK] = [True, False]
COLOR_NAMES = ["black", "white"]
WHITE_COLOR = (255, 253, 208)
BLACK_COLOR = (0, 102, 204)

PieceType = int
PIECE_TYPES = [PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING] = range(1, 7)
PIECE_NAMES = [None, "pawn", "knight", "bishop", "rook", "queen", "king"]


def color_type_to_name(color_type: ColorType) -> str:
    return COLOR_NAMES[color_type]


def color_name_to_type(color_name: str) -> ColorType:
    return COLOR_NAMES.index(color_name)


def piece_type_to_name(piece_type: PieceType) -> str:
    return PIECE_NAMES[piece_type]


def piece_name_to_type(piece_name: str) -> PieceType:
    return PIECE_NAMES.index(piece_name)


def load_images():
    for piece in PIECE_TYPES:
        for color in COLORS:
            IMAGES[color][piece] = pygame.transform.scale(
                pygame.image.load(f'images/{piece_type_to_name(piece)}-{color_type_to_name(color)}.svg'),
                (SQUARE_SIZE, SQUARE_SIZE)
            )


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
        # self.draw_game_state()
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
        self.draw_board()
        load_images()

    def draw_board(self):
        """Draws the squares on the board"""
        colors = [pygame.Color(WHITE_COLOR), pygame.Color(BLACK_COLOR)]
        for row in range(DIMENSION):
            for column in range(DIMENSION):
                color = colors[(row + column) % 2]  # Light squares have even parity, dark have odd parity
                pygame.draw.rect(self.screen,
                                 color,
                                 pygame.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                                 )

    def draw_game_state(self):
        """Draws the pieces on the board from the current game state."""
        for row in range(DIMENSION):
            for column in range(DIMENSION):
                piece = model.board[row, column]
                if piece != '-':
                    self.screen.blit(IMAGES[piece],
                                     pygame.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
