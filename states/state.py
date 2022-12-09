
import pygame

class State:
    def __init__(self, game):
        # Get the display surface
        self.display_surface = pygame.display.get_surface()
        self.game = game

        self.creation_time = pygame.time.get_ticks()