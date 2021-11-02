import pygame
import model
from eventmanager import *

WIDTH = HEIGHT = 800
DIMENSION = 8
SQUARE_SIZE = HEIGHT // DIMENSION


class Keyboard:
    """
    Handles Mouse input.
    """

    def __init__(self, event_manager, model):
        """
        :param event_manager: Allows posting messages to the event queue.
        :param model: a strong reference to the game Model.
        """
        self.event_manager = event_manager
        event_manager.register_listener(self)
        self.model = model

    def notify(self, event):
        """
        Receive events posted to the message queue.
        """

        if isinstance(event, TickEvent):
            # Called for each game tick. We check out keyboard presses here.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.event_manager.post(QuitEvent())
                # handle key down events
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.event_manager.post(QuitEvent())
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.select_piece(pos)
                    self.event_manager.post(InputEvent(pos))

    def select_piece(self, pos):
        column_index = pos[0] // SQUARE_SIZE
        row_index = pos[1] // SQUARE_SIZE

        if self.model.selected_piece:
            self.model.selected_piece.is_selected = False

        selected_piece = self.model.board[row_index][column_index]
        selected_piece.is_selected = not selected_piece.is_selected
        print(selected_piece)
        print(selected_piece.is_selected)
        self.model.selected_piece = selected_piece

        # self.model.selected_square_index = row_index, column_index

