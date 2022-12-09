import pygame
from states.transitions.transitionState import TransitionState
from config.settings import *


class CircleTransitionState(TransitionState):

    def __init__(self, game, transition_mode, next_states = []):
        super().__init__(game, transition_mode, next_states)


    def draw(self):
        self.game.states.element_before(self).draw() 
        self.draw_circle_transition()


    def draw_circle_transition(self): 

        self.transition_time += self.transition_speed * SCALE_FACTOR

        if self.transition_mode == TRANSITION_MODE_IN:
            radius = self.transition_time 
        else:
            radius = self.transition_delay - self.transition_time 
        radius *= SCALE_FACTOR

        w = self.display_surface.get_width() / 2
        h = self.display_surface.get_height() / 2

        pygame.draw.circle(surface = self.display_surface, 
                            color = TRANSITION_COLOR, 
                            radius = radius,
                            center = (w, h))
