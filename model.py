from copy import deepcopy
from constants import *
import pygame
from eventmanager import *
from board import Board
from pieces import Blank
from castling_rights import CastlingRights

COLORS = [WHITE, BLACK] = [True, False]
COLOR_NAMES = ["black", "white"]


def get_square_behind(piece):
    if piece.COLOR == WHITE:
        return piece.row + 1, piece.column
    elif piece.COLOR == BLACK:
        return piece.row - 1, piece.column


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
        self.en_passant_move_log = []  # Did an en passant move happen?
        self.castle_move_log = []  # Did a castling move happen?
        self.castling_rights_log = []

        self.white_king = self.board[7][4]
        self.black_king = self.board[0][4]

        self.en_passant_possible_white = False
        self.en_passant_move_white = ()
        self.en_passant_possible_black = False
        self.en_passant_move_black = ()

        self.white_castling_rights = CastlingRights(True, True)
        self.black_castling_rights = CastlingRights(True, True)

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

    def swap(self, blank_piece, selected_piece):
        blank_piece.row, selected_piece.row = selected_piece.row, blank_piece.row
        blank_piece.column, selected_piece.column = selected_piece.column, blank_piece.column

        self.board[blank_piece.row][blank_piece.column] = blank_piece

        # Pawn Promotion
        if selected_piece.TYPE == PAWN and selected_piece.should_promote():
            selected_piece = selected_piece.transform_to_queen()

        self.update_en_passant_status(blank_piece.row, selected_piece)

        self.board[selected_piece.row][selected_piece.column] = selected_piece

    def update_en_passant_status(self, blank_piece_row, selected_piece):
        if selected_piece.TYPE == PAWN and selected_piece.moved_two_squares(blank_piece_row):
            if selected_piece.COLOR == WHITE:
                self.en_passant_possible_black = True
                self.en_passant_move_black = get_square_behind(selected_piece)
            elif selected_piece.COLOR == BLACK:
                self.en_passant_possible_white = True
                self.en_passant_move_white = get_square_behind(selected_piece)

    @staticmethod
    def swap_with_board(blank_piece, selected_piece, board):
        blank_piece.row, selected_piece.row = selected_piece.row, blank_piece.row
        blank_piece.column, selected_piece.column = selected_piece.column, blank_piece.column

        board[blank_piece.row][blank_piece.column] = blank_piece

        # Pawn Promotion
        if selected_piece.TYPE == PAWN and selected_piece.should_promote():
            selected_piece = selected_piece.transform_to_queen()

        board[selected_piece.row][selected_piece.column] = selected_piece

    def capture(self, captured_piece, taker_piece):
        self.board[taker_piece.row][taker_piece.column] = Blank(taker_piece.row, taker_piece.column)

        taker_piece.row, taker_piece.column = captured_piece.row, captured_piece.column

        # Pawn Promotion
        if taker_piece.TYPE == PAWN and taker_piece.should_promote():
            taker_piece = taker_piece.transform_to_queen()

        self.board[taker_piece.row][taker_piece.column] = taker_piece

    @staticmethod
    def capture_with_board(captured_piece, taker_piece, board):
        board[taker_piece.row][taker_piece.column] = Blank(taker_piece.row, taker_piece.column)

        taker_piece.row, taker_piece.column = captured_piece.row, captured_piece.column

        # Pawn Promotion
        if taker_piece.TYPE == PAWN and taker_piece.should_promote():
            taker_piece = taker_piece.transform_to_queen()

        board[taker_piece.row][taker_piece.column] = taker_piece

    def append_move(self, selected_piece, clicked_piece):
        is_en_passant_move = self.is_en_passant_move(clicked_piece, selected_piece)
        self.en_passant_move_log.append(is_en_passant_move)

        is_kingside_castle_move = self.is_kingside_castle_move(clicked_piece, selected_piece)
        is_queenside_castle_move = self.is_queenside_castle_move(clicked_piece, selected_piece)
        self.castle_move_log.append(is_kingside_castle_move or is_queenside_castle_move)

        self.castling_rights_log.append((deepcopy(self.white_castling_rights), deepcopy(self.black_castling_rights)))

        if is_en_passant_move:
            self.move_log.append((selected_piece, self.get_piece_in_front(clicked_piece)))
        elif is_kingside_castle_move:
            self.move_log.append((self.get_kingside_castle_rook_move_copy()))
        elif is_queenside_castle_move:
            self.move_log.append(self.get_queenside_castle_rook_move_copy())
        self.move_log.append((selected_piece, clicked_piece))

    def get_pseudo_legal_moves(self):
        pseudo_legal_moves = self.selected_piece.get_pseudo_legal_moves(self.board)

        if self.selected_piece.TYPE == PAWN and self.is_en_passant_possible():
            pseudo_legal_moves = self.update_pseudo_legal_moves_for_en_passant(pseudo_legal_moves,
                                                                               self.selected_piece,
                                                                               self.board)

        return pseudo_legal_moves

    def get_legal_moves(self):
        pseudo_legal_moves = self.get_pseudo_legal_moves()
        legal_moves = self.remove_illegal_moves(pseudo_legal_moves)
        legal_moves = self.update_for_castling_moves(legal_moves)

        return legal_moves

    def remove_illegal_moves(self, pseudo_legal_moves):
        legal_moves = set()
        for move in pseudo_legal_moves:
            board_copy, white_king, black_king = self.copy_board_and_kings()
            self.try_pseudo_legal_move(board_copy, move)
            white_king_check_status, black_king_check_status = self.get_check_status_with_board_and_kings(board_copy,
                                                                                                          white_king,
                                                                                                          black_king)
            if self.color_to_move == WHITE:
                in_check = white_king_check_status
            else:
                in_check = black_king_check_status

            if not in_check:
                legal_moves.add(move)
        return legal_moves

    def get_check_status(self):
        white_king_check_status = self.white_king.get_check_status(self.board)
        black_king_check_status = self.black_king.get_check_status(self.board)
        return white_king_check_status, black_king_check_status

    @staticmethod
    def get_check_status_with_board_and_kings(board, white_king, black_king):
        white_king_check_status = white_king.get_check_status(board)
        black_king_check_status = black_king.get_check_status(board)
        return white_king_check_status, black_king_check_status

    def update_check_status(self):
        self.white_king.in_check, self.black_king.in_check = self.get_check_status()

    def try_pseudo_legal_move(self, board_copy, move):
        target_piece_row, target_piece_column = move
        target_piece = board_copy[target_piece_row][target_piece_column]

        selected_piece_row, selected_piece_column = self.selected_piece.row, self.selected_piece.column
        selected_piece_copy = board_copy[selected_piece_row][selected_piece_column]
        if target_piece.TYPE == BLANK:
            self.swap_with_board(target_piece, selected_piece_copy, board_copy)
        else:
            self.capture_with_board(target_piece, selected_piece_copy, board_copy)

    def copy_board_and_kings(self):
        board_copy = deepcopy(self.board)

        white_king_row, white_king_column = self.white_king.row, self.white_king.column
        black_king_row, black_king_column = self.black_king.row, self.black_king.column

        white_king = board_copy[white_king_row][white_king_column]
        black_king = board_copy[black_king_row][black_king_column]

        return board_copy, white_king, black_king

    def update_pseudo_legal_moves_for_en_passant(self, pseudo_legal_moves, selected_pawn, board):
        if selected_pawn.COLOR == WHITE and self.en_passant_possible_white:
            pseudo_legal_moves = selected_pawn.update_pseudo_legal_moves_for_en_passant_white(pseudo_legal_moves,
                                                                                              board,
                                                                                              self.en_passant_move_white)
        elif selected_pawn.COLOR == BLACK and self.en_passant_possible_black:
            pseudo_legal_moves = selected_pawn.update_pseudo_legal_moves_for_en_passant_black(pseudo_legal_moves,
                                                                                              board,
                                                                                              self.en_passant_move_black)
        return pseudo_legal_moves

    def is_en_passant_possible(self):
        return self.en_passant_possible_white or self.en_passant_possible_black

    def is_en_passant_move(self, blank_piece, selected_piece):
        is_en_passant_move = False
        if selected_piece.COLOR == WHITE:
            if selected_piece.TYPE == PAWN and (blank_piece.row, blank_piece.column) == self.en_passant_move_white:
                is_en_passant_move = True

        elif selected_piece.COLOR == BLACK:
            if selected_piece.TYPE == PAWN and (blank_piece.row, blank_piece.column) == self.en_passant_move_black:
                is_en_passant_move = True

        return is_en_passant_move

    def capture_en_passant(self, blank_piece, taker_piece):
        captured_piece = self.get_piece_in_front(blank_piece)
        self.capture(captured_piece, taker_piece)
        self.swap(blank_piece, taker_piece)

    def get_piece_in_front(self, blank_piece):
        if self.color_to_move == WHITE:
            captured_piece = self.board[blank_piece.row + 1][blank_piece.column]
        elif self.color_to_move == BLACK:
            captured_piece = self.board[blank_piece.row - 1][blank_piece.column]
        return captured_piece

    def is_castling_kingside_possible(self):
        if self.color_to_move == WHITE:
            return self.white_castling_rights.can_castle_kingside
        elif self.color_to_move == BLACK:
            return self.black_castling_rights.can_castle_kingside

    def is_castling_queenside_possible(self):
        if self.color_to_move == WHITE:
            return self.white_castling_rights.can_castle_queenside
        elif self.color_to_move == BLACK:
            return self.black_castling_rights.can_castle_queenside

    def update_castling_rights(self):
        if self.selected_piece.TYPE == KING:
            self.disable_castling_rights_after_king_move(self.selected_piece)
        if self.selected_piece.TYPE == ROOK:
            self.disable_castling_rights_after_rook_move(self.selected_piece)

    def disable_castling_rights_after_rook_move(self, selected_piece):
        if selected_piece.COLOR == WHITE:
            if (selected_piece.row, selected_piece.column) == (7, 7):
                self.white_castling_rights.can_castle_kingside = False
            elif (selected_piece.row, selected_piece.column) == (7, 0):
                self.white_castling_rights.can_castle_queenside = False
        elif selected_piece.COLOR == BLACK:
            if (selected_piece.row, selected_piece.column) == (0, 7):
                self.black_castling_rights.can_castle_kingside = False
            elif (selected_piece.row, selected_piece.column) == (0, 0):
                self.black_castling_rights.can_castle_queenside = False

    def disable_castling_rights_after_king_move(self, selected_piece):
        if selected_piece.COLOR == WHITE:
            self.white_castling_rights.can_castle_kingside = False
            self.white_castling_rights.can_castle_queenside = False
        elif selected_piece.COLOR == BLACK:
            self.black_castling_rights.can_castle_kingside = False
            self.black_castling_rights.can_castle_queenside = False

    def update_for_castling_moves(self, legal_moves):
        if self.selected_piece.TYPE == KING and self.is_castling_kingside_possible():
            legal_moves = self.update_legal_moves_for_kingside_castling(legal_moves, self.selected_piece)

        if self.selected_piece.TYPE == KING and self.is_castling_queenside_possible():
            legal_moves = self.update_pseudo_legal_moves_for_queenside_castling(legal_moves, self.selected_piece)

        return legal_moves

    def update_legal_moves_for_kingside_castling(self, legal_moves, selected_king):
        if selected_king.in_check or not self.are_kingside_squares_blank(selected_king):
            return legal_moves

        castling_moves = {(selected_king.row, selected_king.column + 1), (selected_king.row, selected_king.column + 2)}
        legal_castling_moves = self.remove_illegal_moves(castling_moves)

        if len(castling_moves) == len(legal_castling_moves):  # Both moves are legal
            legal_moves.add((selected_king.row, selected_king.column + 2))
        return legal_moves

    def are_kingside_squares_blank(self, selected_king):
        return (self.board[selected_king.row][selected_king.column + 1].TYPE == BLANK
                and self.board[selected_king.row][selected_king.column + 2].TYPE == BLANK)

    def update_pseudo_legal_moves_for_queenside_castling(self, legal_moves, selected_king):
        if selected_king.in_check or not self.are_queenside_squares_blank(selected_king):
            return legal_moves

        castling_moves = {(selected_king.row, selected_king.column - 1), (selected_king.row, selected_king.column - 2)}
        legal_castling_moves = self.remove_illegal_moves(castling_moves)

        if len(castling_moves) == len(legal_castling_moves):  # Both moves are legal
            legal_moves.add((selected_king.row, selected_king.column - 2))
        return legal_moves

    def are_queenside_squares_blank(self, selected_king):
        return (self.board[selected_king.row][selected_king.column - 1].TYPE == BLANK
                and self.board[selected_king.row][selected_king.column - 2].TYPE == BLANK
                and self.board[selected_king.row][selected_king.column - 3].TYPE == BLANK)

    def is_kingside_castle_move(self, clicked_piece, selected_piece):
        is_kingside_castle_move = False

        if selected_piece.TYPE == KING and selected_piece.is_two_squares_to_the_right(clicked_piece):
            is_kingside_castle_move = True

        return is_kingside_castle_move

    def is_queenside_castle_move(self, clicked_piece, selected_piece):
        is_queenside_castle_move = False

        if selected_piece.TYPE == KING and selected_piece.is_two_squares_to_the_left(clicked_piece):
            is_queenside_castle_move = True

        return is_queenside_castle_move

    def castle_kingside(self, blank_piece, selected_king):
        self.swap(blank_piece, selected_king)

        end_square, kingside_rook = self.get_kingside_castle_rook_move()

        self.swap(end_square, kingside_rook)

    def get_kingside_castle_rook_move(self):
        if self.color_to_move == WHITE:
            kingside_rook = self.board[7][7]
            end_square = self.board[7][5]
        else:  # Black to move
            kingside_rook = self.board[0][7]
            end_square = self.board[0][5]
        return end_square, kingside_rook

    def get_kingside_castle_rook_move_copy(self):
        if self.color_to_move == WHITE:
            kingside_rook = self.board[7][7]
            end_square = self.board[7][5]
        else:  # Black to move
            kingside_rook = self.board[0][7]
            end_square = self.board[0][5]

        kingside_rook_copy = deepcopy(kingside_rook)
        end_square_copy = deepcopy(end_square)
        return kingside_rook_copy, end_square_copy

    def castle_queenside(self, blank_piece, selected_king):
        self.swap(blank_piece, selected_king)

        end_square, queenside_rook = self.get_queenside_castle_rook_move()

        self.swap(end_square, queenside_rook)

    def get_queenside_castle_rook_move(self):
        if self.color_to_move == WHITE:
            queenside_rook = self.board[7][0]
            end_square = self.board[7][3]
        else:  # Black to move
            queenside_rook = self.board[0][0]
            end_square = self.board[0][3]

        return end_square, queenside_rook

    def get_queenside_castle_rook_move_copy(self):
        if self.color_to_move == WHITE:
            queenside_rook = self.board[7][0]
            end_square = self.board[7][3]
        else:  # Black to move
            queenside_rook = self.board[0][0]
            end_square = self.board[0][3]

        queenside_rook_copy = deepcopy(queenside_rook)
        end_square_copy = deepcopy(end_square)

        return queenside_rook_copy, end_square_copy

    def undo_castling_rights(self):
        self.white_castling_rights, self.black_castling_rights = self.castling_rights_log.pop()
