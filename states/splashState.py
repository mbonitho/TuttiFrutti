import pygame
from settings import *
from states.state import State
from utils.miscellaneous import draw_rect_alpha


class SplashState(State):

    def __init__(self, game):

        self.font_size = int(UI_FONT_SIZE  * SCALE_FACTOR * 0.7)
        self.font = pygame.font.Font(UI_FONT, self.font_size)

        self.game = game
        self.display_surface = pygame.display.get_surface()
        self.rect = self.display_surface.get_rect()
        
        self.logo_image = pygame.image.load(f'./graphics/logo.png').convert_alpha() 
        self.logo_rect = self.logo_image.get_rect(center= self.rect.center) 

        self.close_cooldown_time = 5000
        self.opened_time = pygame.time.get_ticks()

        self.alpha = 0
        self.step = 255 / 800


    def activate_cooldown(self):
        if pygame.time.get_ticks() - self.opened_time > self.close_cooldown_time:
            self.game.states.pop()


    def input(self):
        pass


    def update_alpha(self):
        self.alpha += self.step
        self.logo_image.set_alpha(self.alpha)


    def draw(self):
        pygame.draw.rect(self.display_surface, '#FFFFFF', self.rect)
        self.display_surface.blit(self.logo_image, (self.logo_rect.x, self.logo_rect.y))


    def run(self):
        self.draw()
        self.update_alpha()
        self.activate_cooldown()