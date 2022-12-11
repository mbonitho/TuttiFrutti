import pygame
from settings import *
from states.state import State
from utils.miscellaneous import draw_rect_alpha


class AboutState(State):

    def __init__(self, game):

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
            "Tutti Frutti",
            "",
            "Utilisez les flèches pour vous déplacer à droite ou à gauche.",
            "Utilisez la touche espace pour activer les éléments du bureau.",
            "La feuille sur le bureau indique les lois en vigueur.",
            "",
            "",
            "2022, Mathieu Bonithon & Josianne de Champlain",
            "Réalisé pour le 12e week-end de programmation Developpez.com",
        ]

        self.papillon_image = pygame.image.load(f'./graphics/papillon.png').convert_alpha() 
        self.papillon_rect = self.papillon_image.get_rect(bottomright= (w - 20, h - 20)) 
        self.tournesol_image = pygame.image.load(f'./graphics/tournesol.png').convert_alpha() 
        self.tournesol_rect = self.tournesol_image.get_rect(bottomright= (w - 100, h - 20)) 

        self.close_cooldown_time = 10000
        self.opened_time = pygame.time.get_ticks()


    def activate_cooldown(self):
        if pygame.time.get_ticks() - self.opened_time > self.close_cooldown_time:
            self.game.states.pop()

            prev = self.game.states.element_before(self)
            if prev != None:
                prev.activation_time = pygame.time.get_ticks() + 1000
                prev.can_activate_selection = False


    def input(self):
        pass


    def draw(self):
        pygame.draw.rect(self.display_surface, '#FFFFFF', self.rect)
        draw_rect_alpha(self.display_surface, (224,224,224, 0), self.rect)

        y = 0
        for _, line in enumerate(self.lines): 

            txt_law_desc_surface = self.font.render(line, True, LAW_SHEET_TEXT_COLOR)
            law_desc_rect = txt_law_desc_surface.get_rect(topleft = self.rect.topleft + pygame.math.Vector2(self.font_size * 0.8 * SCALE_FACTOR, y))
            self.display_surface.blit(txt_law_desc_surface, law_desc_rect)
            y += self.font_size  * SCALE_FACTOR

        self.display_surface.blit(self.papillon_image, (self.papillon_rect.x, self.papillon_rect.y))
        self.display_surface.blit(self.tournesol_image, (self.tournesol_rect.x, self.tournesol_rect.y))


    def run(self):
        self.draw()
        self.input()
        self.activate_cooldown()