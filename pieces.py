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

    def get_legal_moves(self, board):
        pass

    def get_pseudo_legal_moves(self, board):
        pass


class Pawn(Piece):
    TYPE = PAWN

    def __init__(self, color, row=-1, column=-1):
        super().__init__(color, row, column)

    def get_legal_moves(self, board):
        moves = set()
        if self.COLOR == WHITE:
            self._get_legal_moves_white(board, moves)
        elif self.COLOR == BLACK:
            self._get_legal_moves_black(board, moves)

    def _get_legal_moves_white(self, board, moves):
        pass

    def get_pseudo_legal_moves(self, board):
        moves = set()
        if self.COLOR == WHITE:
            self._check_forward_moves_white(board, moves)
            self._check_captures_white(board, moves)
        elif self.COLOR == BLACK:
            self._check_forward_moves_black(board, moves)
            self._check_captures_black(board, moves)
        # TODO: Pawn Promotions
        return moves

    def _check_forward_moves_white(self, board, moves):
        if board[self.row - 1][self.column].TYPE == BLANK:  # One square
            moves.add((self.row - 1, self.column))
            # Needs to be nested, because need both squares to be empty
            if self.row == 6 and board[self.row - 2][self.column].TYPE == BLANK:  # Two squares
                moves.add((self.row - 2, self.column))

    def _check_forward_moves_black(self, board, moves):
        if board[self.row + 1][self.column].TYPE == BLANK:  # One square
            moves.add((self.row + 1, self.column))
            # Needs to be nested, because need both squares to be empty
            if self.row == 1 and board[self.row + 2][self.column].TYPE == BLANK:  # Two squares
                moves.add((self.row + 2, self.column))

    def _check_captures_white(self, board, moves):
        if self.column > 0:  # Left captures, not on edge of the board
            left_diagonal_piece = board[self.row - 1][self.column - 1]
            if left_diagonal_piece.TYPE != BLANK and left_diagonal_piece.COLOR == BLACK:
                moves.add((left_diagonal_piece.row, left_diagonal_piece.column))
        if self.column < len(board) - 1:  # Right captures
            right_diagonal_piece = board[self.row - 1][self.column + 1]
            if right_diagonal_piece.TYPE != BLANK and right_diagonal_piece.COLOR == BLACK:
                moves.add((right_diagonal_piece.row, right_diagonal_piece.column))

    def _check_captures_black(self, board, moves):
        if self.column > 0:  # Left captures
            left_diagonal_piece = board[self.row + 1][self.column - 1]
            if left_diagonal_piece.TYPE != BLANK and left_diagonal_piece.COLOR == WHITE:
                moves.add((left_diagonal_piece.row, left_diagonal_piece.column))
        if self.column < len(board) - 1:  # Right captures
            right_diagonal_piece = board[self.row + 1][self.column + 1]
            if right_diagonal_piece.TYPE != BLANK and right_diagonal_piece.COLOR == WHITE:
                moves.add((right_diagonal_piece.row, right_diagonal_piece.column))

    def should_promote(self):
        should_promote = False

        if (self.COLOR == WHITE and self.row == 0) or (self.COLOR == BLACK and self.row == 8):
            should_promote = True

        return should_promote

    def transform_to_queen(self):
        queen = Queen(self.COLOR, self.row, self.column)
        return queen

    def moved_two_squares(self, blank_piece_row):
        return abs(self.row - blank_piece_row) == 2

    def update_pseudo_legal_moves_for_en_passant_white(self, pseudo_legal_moves, board, en_passant_move):
        left_diagonal_square = (self.row - 1, self.column - 1) if self.column > 0 else ()
        right_diagonal_square = (self.row - 1, self.column + 1) if self.column < len(board) - 1 else ()
        if en_passant_move in {left_diagonal_square, right_diagonal_square}:
            pseudo_legal_moves.add(en_passant_move)

        return pseudo_legal_moves

    def update_pseudo_legal_moves_for_en_passant_black(self, pseudo_legal_moves, board, en_passant_move):
        left_diagonal_square = (self.row + 1, self.column - 1) if self.column > 0 else ()
        right_diagonal_square = (self.row + 1, self.column + 1) if self.column < len(board) - 1 else ()
        if en_passant_move in {left_diagonal_square, right_diagonal_square}:
            pseudo_legal_moves.add(en_passant_move)

        return pseudo_legal_moves


class Knight(Piece):
    TYPE = KNIGHT

    def __init__(self, color, row=-1, column=-1):
        super().__init__(color, row, column)

    def get_pseudo_legal_moves(self, board):
        moves = set()
        directions = [(-1, -2), (-1, 2), (1, -2), (1, 2), (-2, -1), (-2, 1), (2, -1), (2, 1)]

        for direction in directions:
            end_row = self.row + direction[0]
            end_column = self.column + direction[1]
            if on_the_board(end_row, end_column):
                end_piece = board[end_row][end_column]
                if end_piece.COLOR != self.COLOR:
                    moves.add((end_piece.row, end_piece.column))
        return moves


class Bishop(Piece):
    TYPE = BISHOP

    def __init__(self, color, row=-1, column=-1):
        super().__init__(color, row, column)

    def get_pseudo_legal_moves(self, board):
        moves = set()

        directions = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
        opposite_color = not self.COLOR

        for direction in directions:
            for num_squares_moved in range(1, len(board)):
                end_row = self.row + direction[0] * num_squares_moved
                end_column = self.column + direction[1] * num_squares_moved
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

        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        opposite_color = not self.COLOR

        for direction in directions:
            for num_squares_moved in range(1, len(board)):
                end_row = self.row + direction[0] * num_squares_moved
                end_column = self.column + direction[1] * num_squares_moved
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


class Queen(Piece):
    TYPE = QUEEN

    def __init__(self, color, row=-1, column=-1):
        super().__init__(color, row, column)

    def get_pseudo_legal_moves(self, board):
        rook = Rook(self.COLOR, self.row, self.column)
        bishop = Bishop(self.COLOR, self.row, self.column)
        return set.union(rook.get_pseudo_legal_moves(board), bishop.get_pseudo_legal_moves(board))


def is_cardinal_piece(piece):
    return piece.TYPE in {ROOK, QUEEN}


def in_range_of_king(end_piece, num_squares_away):
    return num_squares_away == 1 and end_piece.TYPE == KING


def in_range_of_pawn(end_piece, num_squares_away, direction):
    if end_piece.COLOR == WHITE:
        return num_squares_away == 1 and end_piece.TYPE == PAWN and direction in {(1, -1), (1, 1)}
    elif end_piece.COLOR == BLACK:
        return num_squares_away == 1 and end_piece.TYPE == PAWN and direction in {(-1, -1), (-1, 1)}


def is_diagonal_piece(piece):
    return piece.TYPE in {BISHOP, QUEEN}


class King(Piece):
    TYPE = KING

    def __init__(self, color, row=-1, column=-1):
        super().__init__(color, row, column)
        self.in_check = False

    def get_pseudo_legal_moves(self, board):
        moves = set()
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1)]

        for direction in directions:
            end_row = self.row + direction[0]
            end_column = self.column + direction[1]
            if on_the_board(end_row, end_column):
                end_piece = board[end_row][end_column]
                if end_piece.COLOR != self.COLOR:
                    moves.add((end_piece.row, end_piece.column))
        return moves

    def get_check_status(self, board):
        in_check = False
        cardinal_status = self._get_check_status_from_cardinal_directions(board)
        diagonal_status = self._get_check_status_from_diagonal_directions(board)
        knight_status = self._get_check_status_from_knights(board)

        if any([cardinal_status, diagonal_status, knight_status]):
            in_check = True

        return in_check

    def _get_check_status_from_cardinal_directions(self, board):
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        opposite_color = not self.COLOR
        for direction in directions:
            for num_squares_away in range(1, len(board)):
                end_row = self.row + direction[0] * num_squares_away
                end_column = self.column + direction[1] * num_squares_away
                if on_the_board(end_row, end_column):
                    end_piece = board[end_row][end_column]
                    if end_piece.COLOR == self.COLOR:
                        break
                    elif end_piece.COLOR == opposite_color:
                        if in_range_of_king(end_piece, num_squares_away) or is_cardinal_piece(end_piece):
                            print("cardinal")
                            print(end_piece.TYPE)
                            print(end_piece.row)
                            print(end_piece.column)
                            return True
                        # if a enemy piece that doesn't check the king is found, stop looking in this direction
                        break
        return False

    def _get_check_status_from_diagonal_directions(self, board):
        directions = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
        opposite_color = not self.COLOR
        for direction in directions:
            for num_squares_away in range(1, len(board)):
                end_row = self.row + direction[0] * num_squares_away
                end_column = self.column + direction[1] * num_squares_away
                if on_the_board(end_row, end_column):
                    end_piece = board[end_row][end_column]
                    if end_piece.COLOR == self.COLOR:
                        break
                    elif end_piece.COLOR == opposite_color:
                        if (in_range_of_king(end_piece, num_squares_away)
                                or in_range_of_pawn(end_piece, num_squares_away, direction)
                                or is_diagonal_piece(end_piece)):
                            print("diagonal")
                            print(end_piece.TYPE)
                            print(end_piece.row)
                            print(end_piece.column)
                            return True
                        # if a enemy piece that doesn't check the king is found, stop looking in this direction
                        break
        return False

    def _get_check_status_from_knights(self, board):
        directions = [(-1, -2), (-1, 2), (1, -2), (1, 2), (-2, -1), (-2, 1), (2, -1), (2, 1)]
        opposite_color = not self.COLOR

        for direction in directions:
            end_row = self.row + direction[0]
            end_column = self.column + direction[1]
            if on_the_board(end_row, end_column):
                end_piece = board[end_row][end_column]
                if end_piece.COLOR == opposite_color and end_piece.TYPE == KNIGHT:
                    print("knight")
                    print(end_piece.TYPE)
                    print(end_piece.row)
                    print(end_piece.column)
                    return True
        return False

    def update_pseudo_legal_moves_for_kingside_castling_white(self, pseudo_legal_moves, board, en_passant_move):
        left_diagonal_square = (self.row - 1, self.column - 1) if self.column > 0 else ()
        right_diagonal_square = (self.row - 1, self.column + 1) if self.column < len(board) - 1 else ()
        if en_passant_move in {left_diagonal_square, right_diagonal_square}:
            pseudo_legal_moves.add(en_passant_move)

        return pseudo_legal_moves


class Blank(Piece):
    TYPE = 0

    def __init__(self, row=-1, column=-1):
        super().__init__(None, row, column)
