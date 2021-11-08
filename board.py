import pygame
from pieces import *
from constants import *


class Board:
    BOARD_WIDTH = 8

    def __init__(self):
        self.board = [
            [Rook(BLACK), Knight(BLACK), Bishop(BLACK), Queen(BLACK), King(BLACK), Bishop(BLACK), Knight(BLACK), Rook(BLACK)],
            [Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK)],
            [Blank(), Blank(), Blank(), Blank(), Blank(), Blank(), Blank(), Blank()],
            [Blank(), Blank(), Blank(), Blank(), Blank(), Blank(), Blank(), Blank()],
            [Blank(), Blank(), Blank(), Blank(), Blank(), Blank(), Blank(), Blank()],
            [Blank(), Blank(), Blank(), Blank(), Blank(), Blank(), Blank(), Blank()],
            [Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE)],
            [Rook(WHITE), Knight(WHITE), Bishop(WHITE), Queen(WHITE), King(WHITE), Bishop(WHITE), Knight(WHITE), Rook(WHITE)]
            ]
        for row in self.board:
            for piece in row:
                piece.row = self.board.index(row)
                piece.column = row.index(piece)


class DebugBoard:
    def __init__(self, board):
        self.board = board

    def __str__(self):
        output = ''
        for row in self.board:
            output += '['
            for piece in row:
                output += f' {PIECE_NAMES[piece.TYPE]}'
            output += ']\n'
        return output

    # TODO: Decide if want a board object in main or just the board list
    # def swap(self, piece1, piece2):
    #     piece1.row, piece2.row = piece2.row, piece1.row
    #     piece1.column, piece2.column = piece2.column, piece1.column
    #
    #     self.board[piece1.row][piece1.column] = piece1
    #     self.board[piece2.row][piece2.column] = piece2
