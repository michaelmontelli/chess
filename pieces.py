import pygame
from piece import Piece, _get_image


class Pawn(Piece):
    WHITE = _get_image("pawn", "white")
    BLACK = _get_image("pawn", "black")

    def __init__(self, image, location):
        super().__init__(image, location)

    def move(self):
        pass


class Knight(Piece):
    WHITE = _get_image("knight", "white")
    BLACK = _get_image("knight", "black")

    def __init__(self, image, location):
        super().__init__(image, location)

    def move(self):
        pass


class Bishop(Piece):
    WHITE = _get_image("bishop", "white")
    BLACK = _get_image("bishop", "black")

    def __init__(self, image, location):
        super().__init__(image, location)

    def move(self):
        pass


class Rook(Piece):
    WHITE = _get_image("rook", "white")
    BLACK = _get_image("rook", "black")

    def __init__(self, image, location):
        super().__init__(image, location)

    def move(self):
        pass


class Queen(Piece):
    WHITE = _get_image("queen", "white")
    BLACK = _get_image("queen", "black")

    def __init__(self, image, location):
        super().__init__(image, location)

    def move(self):
        pass


class King(Piece):
    WHITE = _get_image("king", "white")
    BLACK = _get_image("king", "black")

    def __init__(self, image, location):
        super().__init__(image, location)

    def move(self):
        pass
