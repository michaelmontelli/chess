ColorType = bool
COLORS = [WHITE, BLACK] = [True, False]
COLOR_NAMES = ["black", "white"]

PieceType = int
PIECE_TYPES = [PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING] = range(1, 7)
PIECE_NAMES = [None, "pawn", "knight", "bishop", "rook", "queen", "king"]


class Piece:
    TYPE = -1

    def __init__(self, color, row=0, column=0):
        self.COLOR = color
        self.row = row
        self.column = column

    def move(self):
        pass


class Pawn(Piece):
    TYPE = PAWN

    def __init__(self, color, row=0, column=0):
        super().__init__(color, row, column)

    def move(self):
        pass


class Knight(Piece):
    TYPE = KNIGHT

    def __init__(self, color, row=0, column=0):
        super().__init__(color, row, column)


class Bishop(Piece):
    TYPE = BISHOP

    def __init__(self, color, row=0, column=0):
        super().__init__(color, row, column)


class Rook(Piece):
    TYPE = ROOK

    def __init__(self, color, row=0, column=0):
        super().__init__(color, row, column)


class Queen(Piece):
    TYPE = QUEEN

    def __init__(self, color, row=0, column=0):
        super().__init__(color, row, column)


class King(Piece):
    TYPE = KING

    def __init__(self, color, row=0, column=0):
        super().__init__(color, row, column)


class Blank(Piece):
    TYPE = 0

    def __init__(self, row=0, column=0):
        super().__init__(row, column)
