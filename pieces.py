import pygame
from piece import Piece
from board import Board


WHITE_STARTING_RANK = 6
BLACK_STARTING_RANK = 1


class Pawn(Piece):
    WHITE_STARTING_LOCATION = [(column_index, WHITE_STARTING_RANK)
                               for column_index in range(Board.BOARD_WIDTH)]
    BLACK_STARTING_LOCATION = [(column_index, BLACK_STARTING_RANK)
                               for column_index in range(Board.BOARD_WIDTH)]

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
