import pygame, sys
from settings import *
from entities.player.playerInfo import PlayerInfo
from states.gameState import GameState
from states.menus.aboutState import AboutState
from states.menus.selectableOptionsScreenState import SelectableOptionsScreenState
from states.transitions.clapTransitionState import ClapTransitionState
from states.readOpeningLetterState import ReadOpeningLetterState

class TitleState(SelectableOptionsScreenState):

    first_game = True

    def __init__(self, game):
        super().__init__(game=game, 
                         has_themed_box=True)

        # Menu Options
        self.options = {'Nouveau jeu' : self.newGame, 
                        'À propos' : self.openAbout,
                        'Quitter' : self.close}

        bg_image = pygame.image.load('./graphics/titre.png').convert_alpha()
        self.background = bg_image
        

    def playMusic(self):
        # Menu music
        pygame.mixer.music.load('./sound/bgm/title.wav')
        pygame.mixer.music.play(-1)


    def newGame(self):
        if self.can_activate_selection:
            pygame.mixer.music.stop()
            self.game.player_info = PlayerInfo() # reset player stats
            self.game.states.push(GameState(self.game))
            self.game.states.force_push(ClapTransitionState(self.game, TRANSITION_MODE_OUT))
            if TitleState.first_game:
                self.game.states.force_push(ReadOpeningLetterState(self.game))
            self.game.increment_day()
            TitleState.first_game = False


    def openAbout(self):
        if self.can_activate_selection:
            self.game.states.force_push(AboutState(self.game))


    def close(self):
        pygame.quit()
        sys.exit()


    def draw(self):

        # draw background
        self.display_surface.blit(self.background, (0,0)) 

        # options
        super().draw()
