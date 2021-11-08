from constants import *


class Piece:
    TYPE = -1

    def __init__(self, color, row=-1, column=-1):
        self.COLOR = color
        self.row = row
        self.column = column

        self.is_selected = False

    def switch_selected_status(self):
        self.is_selected = not self.is_selected

    def move(self):
        pass


class Pawn(Piece):
    TYPE = PAWN

    def __init__(self, color, row=-1, column=-1):
        super().__init__(color, row, column)

    def move(self):
        pass


class Knight(Piece):
    TYPE = KNIGHT

    def __init__(self, color, row=-1, column=-1):
        super().__init__(color, row, column)


class Bishop(Piece):
    TYPE = BISHOP

    def __init__(self, color, row=-1, column=-1):
        super().__init__(color, row, column)


class Rook(Piece):
    TYPE = ROOK

    def __init__(self, color, row=-1, column=-1):
        super().__init__(color, row, column)


class Queen(Piece):
    TYPE = QUEEN

    def __init__(self, color, row=-1, column=-1):
        super().__init__(color, row, column)


class King(Piece):
    TYPE = KING

    def __init__(self, color, row=-1, column=-1):
        super().__init__(color, row, column)


class Blank(Piece):
    TYPE = 0

    def __init__(self, row=-1, column=-1):
        super().__init__(None, row, column)
