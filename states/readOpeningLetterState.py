import pygame
from settings import *
from states.state import State
from utils.miscellaneous import draw_rect_alpha


class ReadOpeningLetterState(State):

    def __init__(self, game, next_states = []):

        self.font_size = int(UI_FONT_SIZE  * SCALE_FACTOR * 0.7)
        self.font = pygame.font.Font(UI_FONT, self.font_size)

        self.game = game
        self.display_surface = pygame.display.get_surface()
        
        # default sheet dimensions
        h = self.display_surface.get_height()
        w = self.display_surface.get_width()
        self.menu_height = h * 0.8
        self.menu_width = w * 0.8
        self.rect = pygame.Rect(w * .1, h * .1, self.menu_width, self.menu_height)

        # text
        self.lines = [
            "Piff,",
            ""
            "Le comité de quartier vous a désigné comme ",
            "nouveau bienveillant observateur de l’immeuble.",
            "Pendant 5 jours, vous devrez appliquer",
            "rigoureusement la loi en signalant tout",
            "comportement illégal aux autorités compétentes.",
            "",
            "Ne laissez rien passer mais attention, car toute fausse", 
            "signalisation sera prélevée directement sur votre paie.",
            "",
            "Bon courage, et que Blédor vous guide.",
            "",
            "Roff, gentil garant du quartier #159A"
        ]

        self.next_states = next_states


    def close(self):
        self.game.states.pop()
        for state in self.next_states:
            state.activation_time = pygame.time.get_ticks() + 1000
            state.can_activate_selection = False
            self.game.states.force_push(state)


    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
            self.close()


    def draw(self):
        pygame.draw.rect(self.display_surface, '#FFFFFF', self.rect)
        draw_rect_alpha(self.display_surface, (224,224,224, 0), self.rect)

        y = 0
        for _, line in enumerate(self.lines): 

            txt_law_desc_surface = self.font.render(line, False, LAW_SHEET_TEXT_COLOR)
            law_desc_rect = txt_law_desc_surface.get_rect(topleft = self.rect.topleft + pygame.math.Vector2(self.font_size * 0.8 * SCALE_FACTOR, y))
            self.display_surface.blit(txt_law_desc_surface, law_desc_rect)
            y += self.font_size  * SCALE_FACTOR


    def run(self):
        self.draw()
        self.input()