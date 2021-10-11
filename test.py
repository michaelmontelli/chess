import pygame
import pygame
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

running = True
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:
            running = False


