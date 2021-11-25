import pygame
from eventmanager import *
from board import Board
from pieces import Blank

COLORS = [WHITE, BLACK] = [True, False]
COLOR_NAMES = ["black", "white"]


class GameEngine:
    """
    Tracks the game state.
    """

    def __init__(self, event_manager):
        """
        event_manager: Allows posting messages to the event queue.

        Attributes:
        running (bool): True while the engine is online. Changed via QuitEvent().
        """
        self.event_manager = event_manager
        event_manager.register_listener(self)
        self.running = False

        self.board = Board().board
        self.selected_piece = None
        self.color_to_move = WHITE
        self.move_log = []

    def notify(self, event):
        """
        Called by an event in the message queue.
        """
        if isinstance(event, QuitEvent):
            self.running = False

    def run(self):
        """
        Starts the game engine loop

        This pumps a Tick event into the message queue for each loop.
        The loop ends when this object hears a QuitEvent in notify().
        """
        self.running = True
        self.event_manager.post(InitializeEvent())
        while self.running:
            new_tick = TickEvent()
            self.event_manager.post(new_tick)

    def swap(self, piece1, piece2):
        piece1.row, piece2.row = piece2.row, piece1.row
        piece1.column, piece2.column = piece2.column, piece1.column

        self.board[piece1.row][piece1.column] = piece1
        self.board[piece2.row][piece2.column] = piece2

    def capture(self, captured_piece, taker_piece):
        self.board[taker_piece.row][taker_piece.column] = Blank(taker_piece.row, taker_piece.column)

        taker_piece.row, taker_piece.column = captured_piece.row, captured_piece.column
        self.board[taker_piece.row][taker_piece.column] = taker_piece

    def append_move(self, piece1, piece2):
        self.move_log.append((piece1, piece2))

    def get_legal_moves(self):
        if self.selected_piece.COLOR == self.color_to_move:
            # TODO: Check if we need to change this to legal_moves
            return self.selected_piece.get_pseudo_legal_moves(self.board)


