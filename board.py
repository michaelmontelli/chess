import pygame
from rank import Rank


class Board:
    BOARD_WIDTH = 8

    def __init__(self):
        self.board = Board.__make_board()

    @staticmethod
    def __make_board():
        board = []
        for row_index in range(Rank.RANK_LENGTH):
            board.append(Rank(row_index))
        return board

    def draw(self):
        for rank in self.board:
            rank.draw()
