import pygame
from states.transitions.transitionState import TransitionState
from settings import *


class ClapTransitionState(TransitionState):

    def __init__(self, game, transition_mode, next_states = []):
        super().__init__(game, transition_mode, next_states)


    def draw(self):
        self.game.states.element_before(self).draw() 
        self.draw_square_transition()


    def draw_square_transition(self):
        self.transition_time += self.transition_speed * SCALE_FACTOR

        width = self.display_surface.get_width()
        height = self.display_surface.get_height() / 2

        rect_top = None
        rect_btm = None

        if self.transition_mode == TRANSITION_MODE_IN: # rectangles "closing"
            rect_top = pygame.Rect(0, -height + self.transition_time, width, height)
            rect_btm = pygame.Rect(0, height * 2 - self.transition_time, width, height)
            if rect_top.bottom == height:
                self.transition_time = self.transition_delay
        else: # rectangles "opening"
            rect_top = pygame.Rect(0, 0 - self.transition_time, width, height)
            rect_btm = pygame.Rect(0, height + self.transition_time, width, height)
            if rect_top.bottom < 0:
                self.transition_time = self.transition_delay

        pygame.draw.rect(surface = self.display_surface, 
                            color = TRANSITION_COLOR, 
                            rect = rect_top)
        pygame.draw.rect(surface = self.display_surface, 
                            color = TRANSITION_COLOR, 
                            rect = rect_btm)
