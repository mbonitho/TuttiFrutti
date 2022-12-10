import pygame, sys
from settings import *
from entities.player.playerInfo import PlayerInfo
from states.gameState import GameState
from states.menus.aboutState import AboutState
from states.menus.selectableOptionsScreenState import SelectableOptionsScreenState
from states.transitions.clapTransitionState import ClapTransitionState
from states.text.textBoxState import TextBoxState

class TitleState(SelectableOptionsScreenState):

    def __init__(self, game):
        super().__init__(game=game, 
                         has_themed_box=True)

        # Menu Options
        self.options = {'Nouveau jeu' : self.newGame, 
                        'Aide et à propos' : self.openAbout,
                        'Quitter' : self.close}


    def newGame(self):
        if self.can_activate_selection:
            self.game.player_info = PlayerInfo() # reset player stats
            self.game.states.push(GameState(self.game))
            self.game.states.force_push(ClapTransitionState(self.game, TRANSITION_MODE_OUT))
            self.game.states.force_push(TextBoxState(self.game, 'JOUR 1'))


    def openAbout(self):
        if self.can_activate_selection:
            self.game.states.force_push(AboutState(self.game))


    def close(self):
        pygame.quit()
        sys.exit()


    def draw(self):
        # options
        super().draw()

        # title text
        title_txt_surface = self.font.render('TUTTI FRUTTI', False, TEXT_COLOR)
        title_rect = title_txt_surface.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0,HEIGHT * .25))
        self.display_surface.blit(title_txt_surface, title_rect)
    