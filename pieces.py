class Piece:
    img = -1

    def __init__(self, row, column):
        self.row = row
        self.column = column

    def move(self):
        pass


class Pawn(Piece):
    def __init__(self, color, location):
        super().__init__(color, location)

    def move(self):
        pass


class Knight(Piece):
    def __init__(self, color, location):
        super().__init__(color, location)


class Bishop(Piece):
    def __init__(self, color, location):
        super().__init__(color, location)


class Rook(Piece):
    def __init__(self, color, location):
        super().__init__(color, location)


class Queen(Piece):
    def __init__(self, color, location):
        super().__init__(color, location)


class King(Piece):
    def __init__(self, color, location):
        super().__init__(color, location)
