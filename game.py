import pygame, sys
from settings import *
from entities.player.playerInfo import PlayerInfo
from states.menus.titleState import TitleState
from states.text.textBoxState import TextBoxState
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

        # get all laws
        self.all_laws = self.get_laws()

        # player stats
        self.player_info = PlayerInfo() 

        self.states = TimedStack()
        self.states.push(TitleState(self))

        self.day_number = 0
        self.current_laws = []
        self.time_of_day = 0
        self.last_hour_change_time = None


    def resetGame(self):
        self.day_number = 0
        self.current_laws = []
        self.time_of_day = 0
        self.last_hour_change_time = pygame.time.get_ticks()
        self.player_info = PlayerInfo()


    def increment_day(self):
        self.day_number += 1
        self.time_of_day = 0
        self.last_hour_change_time = pygame.time.get_ticks()
        if self.day_number <= NUMBER_OF_DAYS:
            self.states.force_push(TextBoxState(self, f'JOUR {self.day_number}'))   
        self.player_info.total_income += self.player_info.current_income
        self.player_info.current_income = self.player_info.base_daily_income

        nb = 2 if self.day_number < 2 else 4
        self.modifyLaws(nb)


    def triggerEndGame(self):
        st1 = TitleState(self)
        self.states.force_push(TextBoxState(self, f'Félicitations! Votre semaine de travail est terminée. Voici votre salaire : {self.player_info.total_income}$', [st1])) 
        self.resetGame()


    def triggerGameOver(self):
        st1 = TitleState(self)
        self.states.force_push(TextBoxState(self, f'Vous avez déshonnoré Blédor, notre leader suprême. Lorsque vous sortirez du camp de réinsertion sociale, essayez de garder votre emploi plus de {self.day_number} jours!', [st1])) 
        self.resetGame()


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
        laws.append(Law(code=LAW_DONT_STOP_MOVING, name='Volontaire', description='Il est interdit de s\'immobiliser'))
        return laws


    def modifyLaws(self, number):

        # remove a law
        if len(self.current_laws) > 0:
            random_law = choice(self.current_laws)
            self.current_laws.remove(random_law)

        # add a law
        while len(self.current_laws) < number:
            found = False
            random_law = None
            while not found:
                random_law = choice(self.all_laws)
                found = random_law.code not in [x.code for x in self.current_laws]
            self.current_laws.append(random_law)


if __name__ == '__main__':
    game = Game()
    game.run()
    