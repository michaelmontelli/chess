from copy import deepcopy
from constants import *
import pygame
from eventmanager import *
from board import Board
from pieces import Blank

COLORS = [WHITE, BLACK] = [True, False]
COLOR_NAMES = ["black", "white"]


class GameEngine:
    """
    Tracks the game state.
    """

    def __init__(self, event_manager):
        """
        event_manager: Allows posting messages to the event queue.

        Attributes:
        running (bool): True while the engine is online. Changed via QuitEvent().
        """
        self.event_manager = event_manager
        event_manager.register_listener(self)
        self.running = False

        self.board = Board().board
        self.selected_piece = None
        self.color_to_move = WHITE
        self.move_log = []

        self.white_king = self.board[7][4]
        self.black_king = self.board[0][4]

    def notify(self, event):
        """
        Called by an event in the message queue.
        """
        if isinstance(event, QuitEvent):
            self.running = False

    def run(self):
        """
        Starts the game engine loop

        This pumps a Tick event into the message queue for each loop.
        The loop ends when this object hears a QuitEvent in notify().
        """
        self.running = True
        self.event_manager.post(InitializeEvent())
        while self.running:
            new_tick = TickEvent()
            self.event_manager.post(new_tick)

    def swap(self, piece1, piece2):
        piece1.row, piece2.row = piece2.row, piece1.row
        piece1.column, piece2.column = piece2.column, piece1.column

        self.board[piece1.row][piece1.column] = piece1
        self.board[piece2.row][piece2.column] = piece2

    def swap_with_board(self, piece1, piece2, board):
        piece1.row, piece2.row = piece2.row, piece1.row
        piece1.column, piece2.column = piece2.column, piece1.column

        board[piece1.row][piece1.column] = piece1
        board[piece2.row][piece2.column] = piece2

    def capture(self, captured_piece, taker_piece):
        self.board[taker_piece.row][taker_piece.column] = Blank(taker_piece.row, taker_piece.column)

        taker_piece.row, taker_piece.column = captured_piece.row, captured_piece.column
        self.board[taker_piece.row][taker_piece.column] = taker_piece

    def capture_with_board(self, captured_piece, taker_piece, board):
        board[taker_piece.row][taker_piece.column] = Blank(taker_piece.row, taker_piece.column)

        taker_piece.row, taker_piece.column = captured_piece.row, captured_piece.column
        board[taker_piece.row][taker_piece.column] = taker_piece

    def append_move(self, piece1, piece2):
        self.move_log.append((piece1, piece2))

    def undo_move(self):
        selected_piece = self.selected_piece
        if selected_piece is not None:
            selected_piece.is_selected = not selected_piece.is_selected

        self.color_to_move = not self.color_to_move
        move_log = self.move_log
        if len(move_log) > 0:
            piece1, piece2 = move_log.pop()

            for piece in (piece1, piece2):
                if piece is not None:
                    self.board[piece.row][piece.column] = piece
                    if piece.TYPE == KING and piece.COLOR == WHITE:
                        self.white_king = piece
                    elif piece.TYPE == KING and piece.COLOR == BLACK:
                        self.black_king = piece

        # # If the move log is empty, it means we are at the first turn of the game.
        # # White always moves first
        if len(move_log) == 0:
            self.color_to_move = True

    def get_pseudo_legal_moves(self):
        if self.selected_piece.COLOR == self.color_to_move:
            # TODO: Check if we need to change this to legal_moves
            return self.selected_piece.get_pseudo_legal_moves(self.board)

    def get_legal_moves(self):
        legal_moves = set()
        pseudo_legal_moves = self.get_pseudo_legal_moves()
        for move in pseudo_legal_moves:
            board_copy, white_king, black_king = self.copy_board_and_kings()
            self.try_pseudo_legal_move(board_copy, move)
            white_king_check_status, black_king_check_status = self.get_check_status_with_board_and_kings(board_copy,
                                                                                                          white_king,
                                                                                                          black_king)
            print("color to move: ", self.color_to_move)
            if self.color_to_move == WHITE:
                in_check = white_king_check_status
            else:
                in_check = black_king_check_status

            if not in_check:
                legal_moves.add(move)
            self.undo_pseudo_legal_move(board_copy, move)

        return legal_moves

    def get_check_status(self):
        white_king_check_status = self.white_king.get_check_status(self.board)
        black_king_check_status = self.black_king.get_check_status(self.board)
        return white_king_check_status, black_king_check_status

    def get_check_status_with_board_and_kings(self, board, white_king, black_king):
        white_king_check_status = white_king.get_check_status(board)
        black_king_check_status = black_king.get_check_status(board)
        return white_king_check_status, black_king_check_status

    def update_check_status(self):
        self.white_king.in_check, self.black_king.in_check = self.get_check_status()

        print(self.color_to_move)
        print("White King: ")
        print("-------------")
        print(f"Location: {self.white_king.row}, {self.white_king.column}")
        print(f"In Check: {self.white_king.in_check}")
        print("Black King: ")
        print("-------------")
        print(f"Location: {self.black_king.row}, {self.black_king.column}")
        print(f"In Check: {self.black_king.in_check}")

    def try_pseudo_legal_move(self, board_copy, move):
        target_piece_row, target_piece_column = move
        target_piece = board_copy[target_piece_row][target_piece_column]

        selected_piece_row, selected_piece_column = self.selected_piece.row, self.selected_piece.column
        selected_piece_copy = board_copy[selected_piece_row][selected_piece_column]
        if target_piece.TYPE == BLANK:
            self.swap_with_board(target_piece, selected_piece_copy, board_copy)
        else:
            self.capture_with_board(target_piece, selected_piece_copy, board_copy)

    def undo_pseudo_legal_move(self, board_copy, move):
        pass

    def copy_board_and_kings(self):
        board_copy = deepcopy(self.board)

        white_king_row, white_king_column = self.white_king.row, self.white_king.column
        black_king_row, black_king_column = self.black_king.row, self.black_king.column

        white_king = board_copy[white_king_row][white_king_column]
        black_king = board_copy[black_king_row][black_king_column]

        return board_copy, white_king, black_king
