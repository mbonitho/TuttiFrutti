import pygame
from settings import *

class ThemedRect:

    def __init__(self, rect):

        self.display_surface = pygame.display.get_surface()
        self.update_rect(rect)


    def update_rect(self, rect):
        self.rect = rect
        outline_inflate = 16 * SCALE_FACTOR * 0.25
        self.shadow_rect = pygame.rect.Rect(self.rect)
        self.shadow_rect.topleft = (self.rect.left + outline_inflate, 
                               self.rect.top + outline_inflate)

        self.outline_rect = self.rect.inflate(outline_inflate, outline_inflate)
        self.outline_rect.center = self.rect.center


    def draw(self):
        pygame.draw.rect(self.display_surface, '#000000', self.shadow_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, self.outline_rect)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, self.rect)
