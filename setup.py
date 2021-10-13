import pygame
from board import Board
from pieces import (Pawn, Knight, Bishop,
                    Rook, Queen, King)


class Setup:
    # def setup_pieces():
    #     self.setup_pawns()
    #     self.setup_knights()
    #     self.setup_bishops()
    #     self.setups_rooks()
    #     self.setup_queen()
    #     self.setup_king()
    #
    # def setup_pawns():
    #     self.setup_white_pawns()
    #     self.setup_black_pawns()

    @staticmethod
    def setup_white_pawns():
        for i in range(Board.BOARD_WIDTH):
            for x, y in Pawn.WHITE_STARTING_LOCATION:
                pawn = Pawn("white", (x * 100, y * 100))
                pawn.draw()

    @staticmethod
    def setup_black_pawns():
        for i in range(Board.BOARD_WIDTH):
            for x, y in Pawn.BLACK_STARTING_LOCATION:
                pawn = Pawn("black", (x * 100, y * 100))
                pawn.draw()

    # TODO: Instead of blitting pieces individually, find way to blit at the same time




