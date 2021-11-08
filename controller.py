import pygame
import model
from eventmanager import *
from board import DebugBoard

WIDTH = HEIGHT = 800
DIMENSION = 8
SQUARE_SIZE = HEIGHT // DIMENSION
COLORS = [WHITE, BLACK] = [True, False]
COLOR_NAMES = ["black", "white"]


class Keyboard:
    """
    Handles Mouse input.
    """

    def __init__(self, event_manager, model):
        """
        :param event_manager: Allows posting messages to the event queue.
        :param model: a strong reference to the game Model.
        """
        self.event_manager = event_manager
        event_manager.register_listener(self)
        self.model = model

    def notify(self, event):
        """
        Receive events posted to the message queue.
        """

        if isinstance(event, TickEvent):
            # Called for each game tick. We check out keyboard presses here.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.event_manager.post(QuitEvent())
                # handle key down events
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.event_manager.post(QuitEvent())
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.handle_mouse_click(pos)
                    self.event_manager.post(InputEvent(pos))

    def select_piece(self, piece):
        previous_selected_piece = self.model.selected_piece
        if previous_selected_piece is not None:
            previous_selected_piece.is_selected = False

        piece.is_selected = True
        self.model.selected_piece = piece

    def handle_mouse_click(self, pos):
        column_index = pos[0] // SQUARE_SIZE
        row_index = pos[1] // SQUARE_SIZE

        clicked_piece = self.model.board[row_index][column_index]
        if clicked_piece.TYPE and clicked_piece.COLOR == self.model.color_to_move:
            self.select_piece(clicked_piece)
        else:    # Player wants to move piece to the selected blank square or capture
            self.handle_turn(clicked_piece)

    def handle_turn(self, clicked_piece):
        if not clicked_piece.TYPE:
            # clicked_piece is a blank piece, the location of where to move
            self.move(clicked_piece)
        else:
            # clicked_piece is a piece of the opposite color
            self.capture(clicked_piece)

    def move(self, clicked_piece):
        previous_selected_piece = self.model.selected_piece
        if previous_selected_piece is not None:
            self.model.swap(clicked_piece, previous_selected_piece)
            self.deselect_previous_piece(previous_selected_piece)

    def capture(self, clicked_piece):
        previous_selected_piece = self.model.selected_piece
        if previous_selected_piece is not None:
            self.model.capture(clicked_piece, previous_selected_piece)
            self.deselect_previous_piece(previous_selected_piece)

    def deselect_previous_piece(self, previous_selected_piece):
        previous_selected_piece.is_selected = False
        self.model.selected_piece = None
        self.model.color_to_move = not self.model.color_to_move








