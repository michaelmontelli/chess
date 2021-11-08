import pygame
from copy import deepcopy
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
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.event_manager.post(QuitEvent())
                    elif event.key == pygame.K_LEFT:
                        if len(self.model.move_log) > 0:
                            self.undo_move()
                        self.event_manager.post(InputEvent(None))
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.handle_mouse_click(pos)
                    self.event_manager.post(InputEvent(pos))

    def handle_mouse_click(self, pos):
        column_index = pos[0] // SQUARE_SIZE
        row_index = pos[1] // SQUARE_SIZE

        clicked_piece = self.model.board[row_index][column_index]
        if clicked_piece.TYPE and clicked_piece.COLOR == self.model.color_to_move:
            self.select_piece(clicked_piece)
        else:    # Player wants to move piece to the selected blank square or capture
            self.handle_turn(clicked_piece)

    def select_piece(self, piece):
        previous_selected_piece = self.model.selected_piece
        if previous_selected_piece is not None:
            previous_selected_piece.is_selected = False

        piece.is_selected = True
        self.model.selected_piece = piece

    def handle_turn(self, clicked_piece):
        previous_selected_piece = self.model.selected_piece
        if previous_selected_piece is not None and previous_selected_piece.COLOR == self.model.color_to_move:
            self.append_move(clicked_piece)
        if not clicked_piece.TYPE:
            # clicked_piece is a blank piece, the location of where to move
            self.move(clicked_piece)
        else:
            # clicked_piece is a piece of the opposite color
            self.capture(clicked_piece)

    def move(self, clicked_piece):
        previous_selected_piece = self.model.selected_piece
        if previous_selected_piece is not None and previous_selected_piece.is_selected:
            self.model.swap(clicked_piece, previous_selected_piece)
            self.deselect_previous_piece(previous_selected_piece)

    def capture(self, clicked_piece):
        previous_selected_piece = self.model.selected_piece
        if previous_selected_piece is not None and previous_selected_piece.is_selected:
            self.model.capture(clicked_piece, previous_selected_piece)
            self.deselect_previous_piece(previous_selected_piece)

    def deselect_previous_piece(self, previous_selected_piece):
        previous_selected_piece.is_selected = False
        self.model.selected_piece = None
        self.model.color_to_move = not self.model.color_to_move

    def undo_move(self):
        selected_piece = self.model.selected_piece
        if selected_piece is not None:
            selected_piece.is_selected = not selected_piece.is_selected
            
        move_log = self.model.move_log
        if len(move_log) > 0:
            piece1, piece2 = move_log[-1]
            move_log.pop()

            for piece in (piece1, piece2):
                if piece is not None:
                    self.model.board[piece.row][piece.column] = piece

        # # If the move log is empty, it means we are at the first turn of the game.
        # # White always moves first
        if len(move_log) == 0:
            self.model.color_to_move = not self.model.color_to_move

    def append_move(self, clicked_piece):
        piece1 = self.model.selected_piece
        piece2 = clicked_piece

        piece1_copy = deepcopy(piece1)
        piece2_copy = deepcopy(piece2)

        for piece in (piece1_copy, piece2_copy):
            if piece is not None:
                piece.is_selected = False

        self.model.append_move(piece1_copy, piece2_copy)








