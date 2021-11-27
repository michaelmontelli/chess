import pygame
from copy import deepcopy
import model
from eventmanager import *
from constants import *
from board import DebugBoard

WIDTH = HEIGHT = 800
DIMENSION = 8
SQUARE_SIZE = HEIGHT // DIMENSION


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
            print("en_passant: ", self.model.en_passant_possible_black)
            print(self.model.en_passant_possible_white or self.model.en_passant_possible_black)

    def select_piece(self, piece):
        previous_selected_piece = self.model.selected_piece
        if previous_selected_piece is not None:
            previous_selected_piece.is_selected = False

        piece.is_selected = True
        self.model.selected_piece = piece
        print(self.model.get_pseudo_legal_moves())
        print(self.model.get_legal_moves())

    def handle_turn(self, clicked_piece):
        previous_selected_piece = self.model.selected_piece
        if previous_selected_piece is not None and previous_selected_piece.COLOR == self.model.color_to_move:
            legal_moves = self.model.get_legal_moves()    # TODO: Change to legal moves()
            # self.model.get_legal_moves()    # TODO: Changed when done implementing
            if (clicked_piece.row, clicked_piece.column) in legal_moves:
                self.process_move(clicked_piece)
                self.append_move(clicked_piece)
                self.model.update_check_status()

    def process_move(self, clicked_piece):
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

    def append_move(self, clicked_piece):
        selected_piece = self.model.selected_piece

        selected_piece_copy = deepcopy(selected_piece)
        clicked_piece_copy = deepcopy(clicked_piece)

        for piece in (selected_piece_copy, clicked_piece_copy):
            if piece is not None:
                piece.is_selected = False

        self.model.append_move(selected_piece_copy, clicked_piece_copy)

    def undo_move(self):
        selected_piece = self.model.selected_piece
        if selected_piece is not None:
            selected_piece.is_selected = not selected_piece.is_selected

        self.model.color_to_move = not self.model.color_to_move
        move_log = self.model.move_log
        if len(move_log) > 0:
            piece1, piece2 = move_log.pop()

            for piece in (piece1, piece2):
                if piece is not None:
                    self.model.board[piece.row][piece.column] = piece
                    if piece.TYPE == KING and piece.COLOR == WHITE:
                        self.model.white_king = piece
                    elif piece.TYPE == KING and piece.COLOR == BLACK:
                        self.model.black_king = piece

        # # If the move log is empty, it means we are at the first turn of the game.
        # # White always moves first
        if len(move_log) == 0:
            self.model.color_to_move = True

        # TODO: Make sure correct
        self.model.update_check_status()
