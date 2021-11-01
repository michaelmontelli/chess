ColorType = bool
COLORS = [WHITE, BLACK] = [True, False]
COLOR_NAMES = ["black", "white"]

PieceType = int
PIECE_TYPES = [PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING] = range(1, 7)
PIECE_NAMES = [None, "pawn", "knight", "bishop", "rook", "queen", "king"]


class Piece:
    TYPE = -1

    def __init__(self, color, location):
        self.color = location
        self.column = location

    def move(self):
        pass


class Pawn(Piece):
    TYPE = PAWN

    def __init__(self, color, location):
        super().__init__(color, location)

    def move(self):
        pass


class Knight(Piece):
    TYPE = KNIGHT

    def __init__(self, color, location):
        super().__init__(color, location)


class Bishop(Piece):
    TYPE = BISHOP

    def __init__(self, color, location):
        super().__init__(color, location)


class Rook(Piece):
    TYPE = ROOK

    def __init__(self, color, location):
        super().__init__(color, location)


class Queen(Piece):
    TYPE = QUEEN

    def __init__(self, color, location):
        super().__init__(color, location)


class King(Piece):
    TYPE = KING
    
    def __init__(self, color, location):
        super().__init__(color, location)
