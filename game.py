import pygame, sys
from settings import *
from entities.player.playerInfo import PlayerInfo
from states.menus.titleState import TitleState
from utils.stack import TimedStack


class Game:

    def __init__(self):

        # general setup
        pygame.init()
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.set_mode((WIDTH * SCALE_FACTOR, HEIGHT * SCALE_FACTOR))#, pygame.FULLSCREEN|pygame.SCALED)
        pygame.display.set_caption('Tutti Frutti')
        self.clock = pygame.time.Clock()

        # player stats
        self.player_info = PlayerInfo() 

        self.states = TimedStack()
        self.states.push(TitleState(self))


    def current_state(self):
        return self.states.peek()


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            self.screen.fill('black')
            curr = self.current_state()
            curr.run()
            curr.input()

            pygame.display.update()
            self.clock.tick(FPS)


    def return_to_title(self):
        self.states.clear()
        self.states.push(TitleState(self))


if __name__ == '__main__':
    game = Game()
    game.run()
    