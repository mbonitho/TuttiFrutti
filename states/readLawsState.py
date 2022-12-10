import pygame
from settings import *
from states.state import State
from utils.miscellaneous import draw_rect_alpha


class ReadLawsState(State):

    def __init__(self, game):

        self.law_name_font_size = int(UI_FONT_SIZE  * SCALE_FACTOR * 1.1)
        self.law_name_font = pygame.font.Font(UI_FONT, self.law_name_font_size)

        self.law_desc_font_size = int(UI_FONT_SIZE  * SCALE_FACTOR * 0.8)
        self.law_desc_font = pygame.font.Font(UI_FONT, self.law_desc_font_size)

        self.game = game
        self.display_surface = pygame.display.get_surface()
        
        # default sheet dimensions
        h = self.display_surface.get_height()
        w = self.display_surface.get_width()
        self.menu_height = h * 0.8
        self.menu_width = w * 0.8
        self.rect = pygame.Rect(w * .1, h * .1, self.menu_width, self.menu_height)


    def close(self):
        self.game.states.pop()


    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
            self.close()


    def draw(self):
        self.game.states.element_before(self).draw() # draw game behind menu

        pygame.draw.rect(self.display_surface, '#FFFFFF', self.rect)

        draw_rect_alpha(self.display_surface, (224,224,224, 0), self.rect)

        y = 0
        for index, law in enumerate(self.game.current_laws): 

            txt_law_name_surface = self.law_name_font.render(law.name, False, LAW_SHEET_TEXT_COLOR)
            law_name_rect = txt_law_name_surface.get_rect(topleft = self.rect.topleft + pygame.math.Vector2(0, y))
            self.display_surface.blit(txt_law_name_surface, law_name_rect)
            y += self.law_name_font_size * 1.1 * SCALE_FACTOR


            txt_law_desc_surface = self.law_desc_font.render(law.description, False, LAW_SHEET_TEXT_COLOR)
            law_desc_rect = txt_law_desc_surface.get_rect(topleft = self.rect.topleft + pygame.math.Vector2(0, y))
            self.display_surface.blit(txt_law_desc_surface, law_desc_rect)
            y += self.law_desc_font_size * 1.1 * SCALE_FACTOR

            y += self.law_desc_font_size * 1.1 * SCALE_FACTOR


    def run(self):
        self.draw()
        self.input()