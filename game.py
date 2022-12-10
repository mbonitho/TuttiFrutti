import pygame, sys
from settings import *
from entities.player.playerInfo import PlayerInfo
from states.menus.titleState import TitleState
from utils.stack import TimedStack
from laws.law import Law
from random import choice

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

        self.day_number = 1
        self.current_laws = []

        # get all laws
        self.all_laws = self.get_laws()

        # temp : add 3 laws
        for i in range(3):
            self.addRandomLaw()


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


    def get_laws(self):
        laws = []
        laws.append(Law(code=LAW_LIGHTS_ALWAYS_ON, name='Éveil', description='La lumière doit rester allumée.'))
        laws.append(Law(code=LAW_NO_MUSIC, name='Paix du silence', description='La musique et le bruit sont interdits.'))
        laws.append(Law(code=LAW_NO_OPENED_WINDOW, name='Respect mutuel', description='Les fenêtres doivent rester fermées.'))
        laws.append(Law(code=LAW_NO_VISIT_OTHER_SPECIES, name='Uniformité', description='Les visites des autres sortes de fruits sont interdites.'))
        laws.append(Law(code=LAW_NO_VISIT_SAME_SPECIES, name='Divergence', description='Les visites de la même sorte de fruits sont interdites.'))
        laws.append(Law(code=LAW_STOP_TO_PRAISE_LEADER_AT_NOON, name='Révérence', description='Les fruits doivent s\'arrêter à midi pour vénérer le leader.'))
        return laws


    def addRandomLaw(self):
        found = False
        random_law = None
        while not found:
            random_law = choice(self.all_laws)
            found = random_law.code not in [x.code for x in self.current_laws]
        self.current_laws.append(random_law)


if __name__ == '__main__':
    game = Game()
    game.run()
    