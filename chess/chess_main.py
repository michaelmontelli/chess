"""Main driver file. Handles user input and displays current GameState."""

import pygame as p
import numpy as np
from chess import engine

WIDTH = HEIGHT = 800
DIMENSION = 8
SQUARE_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
WHITE = (255, 253, 208)
BLACK = (0, 102, 204)
IMAGES = {}


def load_images():
    """Load images into our global images dictionary."""
    piece_names = ['pawn', 'knight', 'bishop', 'rook', 'queen', 'king']
    colors = ['white', 'black']
    fen_piece_names = {
        'pawn': 'p',
        'knight': 'n',
        'bishop': 'b',
        'rook': 'r',
        'queen': 'q',
        'king': 'k'
    }
    for piece_name in piece_names:
        for color in colors:
            if color == 'white':
                IMAGES[fen_piece_names[piece_name].upper()] = p.transform.scale(
                    p.image.load(f'images/{piece_name}-{color}.svg'), (SQUARE_SIZE, SQUARE_SIZE))
            else:
                IMAGES[fen_piece_names[piece_name]] = p.transform.scale(
                    p.image.load(f'images/{piece_name}-{color}.svg'), (SQUARE_SIZE, SQUARE_SIZE))


def main():
    """Handle user input and graphics."""
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    board = engine.Board()
    load_images()
    running = True
    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
        draw_game_state(screen, board)
        clock.tick(MAX_FPS)
        p.display.flip()


def draw_game_state(screen, game_state):
    draw_board(screen)
    # TODO: Add in piece highlighting when clicked or possible moves?
    draw_pieces(screen, game_state.board)


def draw_board(screen):
    """Draws the squares on the board"""
    colors = [p.Color(WHITE), p.Color(BLACK)]
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            color = colors[(row + column) % 2]  # Light squares have even parity, dark have odd parity
            p.draw.rect(screen, color, p.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def draw_pieces(screen, board):
    """Draws the pieces on the board from the current game state."""
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row, column]
            if piece != '-':
                screen.blit(IMAGES[piece], p.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


if __name__ == '__main__':
    main()