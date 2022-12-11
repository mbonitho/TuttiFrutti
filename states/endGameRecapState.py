import pygame
from settings import *
from states.state import State
from utils.miscellaneous import draw_rect_alpha


class EndGameRecapState(State):

    def __init__(self, game):

        self.day_number_font_size = int(UI_FONT_SIZE  * SCALE_FACTOR * 0.7)
        self.day_number_font = pygame.font.Font(UI_FONT, self.day_number_font_size)

        self.day_event_font_size = int(UI_FONT_SIZE  * SCALE_FACTOR * 0.5)
        self.day_event_font = pygame.font.Font(UI_FONT, self.day_event_font_size)

        self.day_subtotal_font_size = int(UI_FONT_SIZE  * SCALE_FACTOR * 0.4)
        self.day_subtotal_font = pygame.font.Font(UI_FONT, self.day_event_font_size)

        self.game = game
        self.display_surface = pygame.display.get_surface()
        
        # default sheet dimensions
        h = self.display_surface.get_height()
        w = self.display_surface.get_width()
        self.menu_height = h * 0.8
        self.menu_width = w * 0.8
        self.rect = pygame.Rect(w * .1, h * .1, self.menu_width, self.menu_height)

        # values
        self.total = self.get_total()


    def get_total(self) -> int:
        total = 0
        index = 1
        while index in self.game.score_counters.keys() and index <= NUMBER_OF_DAYS:

            total +=  self.game.score_counters[index].get_day_score()

            index += 1
        
        return total

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

        x = 0
        y = 0
        index = 1
        while index in self.game.score_counters.keys() and index <= NUMBER_OF_DAYS:
            sc = self.game.score_counters[index]

            if index == 4:
                y = 0
                x = 400

            # display day number
            txt_day_name_surface = self.day_number_font.render(f'Jour {index}:', True, LAW_SHEET_TEXT_COLOR)
            rect_day_name = txt_day_name_surface.get_rect(topleft = self.rect.topleft + pygame.math.Vector2(x, y))
            self.display_surface.blit(txt_day_name_surface, rect_day_name)
            y += self.day_number_font_size * 1.1 * SCALE_FACTOR
            
            # display good arrests
            txt_good_arrests = self.day_event_font.render(f'Arrestations réussies: {sc.good}', True, LAW_SHEET_TEXT_COLOR)
            rect_good_arrests = txt_good_arrests.get_rect(topleft = self.rect.topleft + pygame.math.Vector2(x, y))
            self.display_surface.blit(txt_good_arrests, rect_good_arrests)
            y += self.day_event_font_size * 1.1 * SCALE_FACTOR

            # display bad arrests
            txt_bad_arrests = self.day_event_font.render(f'Arrestations ratées: {sc.bad}', True, LAW_SHEET_TEXT_COLOR)
            rect_bad_arrests = txt_bad_arrests.get_rect(topleft = self.rect.topleft + pygame.math.Vector2(x, y))
            self.display_surface.blit(txt_bad_arrests, rect_bad_arrests)
            y += self.day_event_font_size * 1.1 * SCALE_FACTOR
            
            # display missed arrests
            txt_missed_arrests = self.day_event_font.render(f'Arrestations manquées: {sc.missed}', True, LAW_SHEET_TEXT_COLOR)
            rect_missed_arrests = txt_missed_arrests.get_rect(topleft = self.rect.topleft + pygame.math.Vector2(x, y))
            self.display_surface.blit(txt_missed_arrests, rect_missed_arrests)
            y += self.day_event_font_size * 1.1 * SCALE_FACTOR

            # display sub_total
            
            txt_day_total_surface = self.day_subtotal_font.render(f'Sous-total: {sc.get_day_score()}', True, LAW_SHEET_TEXT_COLOR)
            rect_day_total = txt_day_total_surface.get_rect(topleft = self.rect.topleft + pygame.math.Vector2(x, y))
            self.display_surface.blit(txt_day_total_surface, rect_day_total)
            y += self.day_event_font_size * 1.1 * SCALE_FACTOR
            y += self.day_event_font_size * 1.1 * SCALE_FACTOR

            index += 1

            txt_game_total_surface = self.day_number_font.render(f'SCORE TOTAL: {self.total}', True, LAW_SHEET_TEXT_COLOR)
            rect_game_total = txt_game_total_surface.get_rect(center = (self.display_surface.get_rect().centerx, self.display_surface.get_rect().height * 0.8))
            self.display_surface.blit(txt_game_total_surface, rect_game_total)
            y += self.day_number_font_size * 1.1 * SCALE_FACTOR


    def run(self):
        self.draw()
        self.input()