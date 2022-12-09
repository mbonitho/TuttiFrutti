import pygame
from states.transitions.transitionState import TransitionState
from config.settings import *


class FallingRectTransitionState(TransitionState):

    def __init__(self, game, transition_mode, next_states = []):
        super().__init__(game, transition_mode, next_states)
        self.transition_delay *= 2

    def draw(self):
        self.game.states.element_before(self).draw() 
        self.draw_falling_square_transition()


    def draw_falling_square_transition(self):
        self.transition_time += self.transition_speed * SCALE_FACTOR

        width = self.display_surface.get_width()
        height = self.display_surface.get_height()

        rect = None

        if self.transition_mode == TRANSITION_MODE_IN: # rectangle going down
            rect = pygame.Rect(0, -height + self.transition_time, width, height)
            if rect.bottom == height:
                self.transition_time = self.transition_delay
        else: # rectangle going up
            rect = pygame.Rect(0, 0 - self.transition_time, width, height)
            if rect.bottom < 0:
                self.transition_time = self.transition_delay

        pygame.draw.rect(surface = self.display_surface, 
                            color = TRANSITION_COLOR, 
                            rect = rect)
