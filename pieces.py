from constants import *


def on_the_board(row, column):
    return 0 <= row < 8 and 0 <= column < 8


class Piece:
    TYPE = -1

    def __init__(self, color, row=-1, column=-1):
        self.COLOR = color
        self.row = row
        self.column = column

        self.is_selected = False

    def switch_selected_status(self):
        self.is_selected = not self.is_selected


class Pawn(Piece):
    TYPE = PAWN

    def __init__(self, color, row=-1, column=-1):
        super().__init__(color, row, column)

    def get_pseudo_legal_moves(self, board):
        moves = set()
        if self.COLOR == WHITE:
            self.check_forward_moves_white(board, moves)
            self.check_captures_white(board, moves)
        elif self.COLOR == BLACK:
            self.check_forward_moves_black(board, moves)
            self.check_captures_black(board, moves)
        # TODO: Pawn Promotions
        return moves

    def check_forward_moves_white(self, board, moves):
        if board[self.row - 1][self.column].TYPE == BLANK:  # One square
            moves.add((self.row - 1, self.column))
            # Needs to be nested, because need both squares to be empty
            if self.row == 6 and board[self.row - 2][self.column].TYPE == BLANK:  # Two squares
                moves.add((self.row - 2, self.column))

    def check_forward_moves_black(self, board, moves):
        if board[self.row + 1][self.column].TYPE == BLANK:  # One square
            moves.add((self.row + 1, self.column))
            # Needs to be nested, because need both squares to be empty
            if self.row == 1 and board[self.row + 2][self.column].TYPE == BLANK:  # Two squares
                moves.add((self.row + 2, self.column))

    def check_captures_white(self, board, moves):
        if self.column > 0:  # Left captures, not on edge of the board
            left_diagonal_piece = board[self.row - 1][self.column - 1]
            if left_diagonal_piece.TYPE != BLANK and left_diagonal_piece.COLOR == BLACK:
                moves.add((left_diagonal_piece.row, left_diagonal_piece.column))
        if self.column < len(board) - 1:  # Right captures
            right_diagonal_piece = board[self.row - 1][self.column + 1]
            if right_diagonal_piece.TYPE != BLANK and right_diagonal_piece.COLOR == BLACK:
                moves.add((right_diagonal_piece.row, right_diagonal_piece.column))

    def check_captures_black(self, board, moves):
        if self.column > 0:  # Left captures
            left_diagonal_piece = board[self.row + 1][self.column - 1]
            if left_diagonal_piece.TYPE != BLANK and left_diagonal_piece.COLOR == WHITE:
                moves.add((left_diagonal_piece.row, left_diagonal_piece.column))
        if self.column < len(board) - 1:  # Right captures
            right_diagonal_piece = board[self.row + 1][self.column + 1]
            if right_diagonal_piece.TYPE != BLANK and right_diagonal_piece.COLOR == WHITE:
                moves.add((right_diagonal_piece.row, right_diagonal_piece.column))


class Knight(Piece):
    TYPE = KNIGHT

    def __init__(self, color, row=-1, column=-1):
        super().__init__(color, row, column)

    def get_pseudo_legal_moves(self, board):
        return set()


class Bishop(Piece):
    TYPE = BISHOP

    def __init__(self, color, row=-1, column=-1):
        super().__init__(color, row, column)

    def get_pseudo_legal_moves(self, board):
        moves = set()

        directions = ((-1, -1), (1, -1), (-1, 1), (1, 1))
        opposite_color = not self.COLOR

        for direction in directions:
            for squares_moved in range(1, len(board)):
                end_row = self.row + direction[0] * squares_moved
                end_column = self.column + direction[1] * squares_moved
                if on_the_board(end_row, end_column):
                    end_piece = board[end_row][end_column]
                    if end_piece.TYPE == BLANK:
                        moves.add((end_piece.row, end_piece.column))
                    elif end_piece.COLOR == opposite_color:
                        moves.add((end_piece.row, end_piece.column))
                        break
                    elif end_piece.COLOR == self.COLOR:
                        break
                else:  # The square is off the board
                    break
        return moves


class Rook(Piece):
    TYPE = ROOK

    def __init__(self, color, row=-1, column=-1):
        super().__init__(color, row, column)

    def get_pseudo_legal_moves(self, board):
        moves = set()

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        opposite_color = not self.COLOR

        for direction in directions:
            for squares_moved in range(1, len(board)):
                end_row = self.row + direction[0] * squares_moved
                end_column = self.column + direction[1] * squares_moved
                if on_the_board(end_row, end_column):
                    end_piece = board[end_row][end_column]
                    if end_piece.TYPE == BLANK:
                        moves.add((end_piece.row, end_piece.column))
                    elif end_piece.COLOR == opposite_color:
                        moves.add((end_piece.row, end_piece.column))
                        break
                    elif end_piece.COLOR == self.COLOR:
                        break
                else:    # The square is off the board
                    break
        return moves


class Queen(Piece):
    TYPE = QUEEN

    def __init__(self, color, row=-1, column=-1):
        super().__init__(color, row, column)

    def get_pseudo_legal_moves(self, board):
        return set()


class King(Piece):
    TYPE = KING

    def __init__(self, color, row=-1, column=-1):
        super().__init__(color, row, column)

    def get_pseudo_legal_moves(self, board):
        return set()


class Blank(Piece):
    TYPE = 0

    def __init__(self, row=-1, column=-1):
        super().__init__(None, row, column)
