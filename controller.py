import pygame
import model
from eventmanager import *


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
                elif event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    self.event_manager.post(InputEvent(pos))

