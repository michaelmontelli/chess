import pygame


class Square:
    # static variables
    WIDTH = 100
    SIZE = (WIDTH, WIDTH)
    LIGHT_COLOR = (255, 253, 208)
    DARK_COLOR = (0, 102, 204)

    def __init__(self, color, location):
        self.color = color
        self.location = location

    def draw(self):
        pygame.draw.rect(pygame.display.get_surface(), self.color, pygame.Rect(self.location, self.SIZE))


class Rank:
    """A row of the chess board, consisting of 8 squares"""

    # TODO: Decide whether rows are 0 or 1 indexed and which is odd and which is even
    # For now, rows are zero indexed and even indices are even
    RANK_LENGTH = 8
    EVEN = 0
    ODD = 1

    def __init__(self, row_index):
        # TODO: Add a comment about what parity is
        self.parity = row_index % 2
        self.row_index = row_index
        if self.parity == Rank.EVEN:
            self.squares = Rank.__make_even_rank(self.row_index)
        else:
            self.squares = Rank.__make_odd_rank(self.row_index)

    @staticmethod
    def __make_even_rank(row_index):
        # Even ranks start with a light square
        rank = []
        for column_index in range(Rank.RANK_LENGTH):
            if column_index % 2 == Rank.EVEN:
                rank.append(Square(Square.LIGHT_COLOR, (column_index * Square.WIDTH, row_index * Square.WIDTH)))
            else:
                rank.append(Square(Square.DARK_COLOR, (column_index * Square.WIDTH, row_index * Square.WIDTH)))
        return rank

    @staticmethod
    def __make_odd_rank(row_index):
        # Odd ranks start with a dark square
        rank = []
        for column_index in range(Rank.RANK_LENGTH):
            if column_index % 2 == Rank.EVEN:
                rank.append(Square(Square.DARK_COLOR, (column_index * Square.WIDTH, row_index * Square.WIDTH)))
            else:
                rank.append(Square(Square.LIGHT_COLOR, (column_index * Square.WIDTH, row_index * Square.WIDTH)))
        return rank

    def draw(self):
        for square in self.squares:
            square.draw()


class Board:
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

