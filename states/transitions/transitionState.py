import pygame
from states.state import State
from settings import *


class TransitionState(State):

    def __init__(self, game, transition_mode, next_states = []):

        super().__init__(game)

        # transitions
        self.transition_time = 0
        self.transition_delay = pygame.display.get_surface().get_height() / 2
        self.transition_mode = transition_mode
        self.transition_speed = 1.4
        self.next_states = next_states


    def input(self):
        return # no input possible during animation


    def draw(self):
        return


    def check_end(self):
        if self.transition_time >= self.transition_delay:
            self.game.states.pop() 
            for state in self.next_states:
                self.game.states.force_push(state)


    def run(self):
        self.draw()
        self.check_end()
        