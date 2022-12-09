import pygame
from config.settings import *
from sprites.cursor import Cursor
from states.state import State
from theming.themedRect import ThemedRect
from utils.mockJoystick import MockJoystick

class PartialMenuState(State):

    def __init__(self, game):

        super().__init__(game)

        # General setup
        self.player_info = game.player_info
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE  * SCALE_FACTOR)

        # Selection system
        self.selection_cooldown_time = 300
        self.selection_index = 0
        self.selection_time = pygame.time.get_ticks() - 1000
        self.can_move_selection = True
        self.cursorL = Cursor()
        self.cursorR = Cursor()

        # activation system
        self.activation_cooldown_time = 300
        self.activation_time = pygame.time.get_ticks() + self.activation_cooldown_time
        self.can_activate_selection = False
        
        # default menu dimensions
        h = self.display_surface.get_height()
        w = self.display_surface.get_width()
        self.menu_height = h * 0.8
        self.menu_width = w * 0.5
        rect = pygame.Rect(w * .1, h * .1, self.menu_width, self.menu_height)
        self.menu_rect = ThemedRect(rect)

        # no option by default
        self.options = {}


    def activateHighlightedOption(self):
        if self.can_activate_selection:
            option_name = list(self.options.keys())[self.selection_index]
            action_to_perform = self.options[option_name]
            action_to_perform()
            self.can_activate_selection = False
            self.activation_time = pygame.time.get_ticks()


    def move_selection_up(self):
        if self.can_move_selection:
            self.selection_index -= 1
            if self.selection_index < 0:
                self.selection_index = len(self.options) - 1
            self.can_move_selection = False
            self.selection_time = pygame.time.get_ticks()


    def move_selection_down(self):
        if self.can_move_selection:
            self.selection_index += 1
            if self.selection_index > len(self.options) - 1:
                self.selection_index = 0
            self.can_move_selection = False
            self.selection_time = pygame.time.get_ticks()


    def selection_cooldown(self):
        if not self.can_move_selection and pygame.time.get_ticks() - self.selection_time > self.selection_cooldown_time:
            self.can_move_selection = True


    def activation_cooldown(self):
        if not self.can_activate_selection and pygame.time.get_ticks() - self.activation_time > self.activation_cooldown_time:
            self.can_activate_selection = True


    def close(self):
        self.game.states.pop()


    def input(self):
        keys = pygame.key.get_pressed()
        joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

        # obtain first player joystick, or dummy joystick if none is connected
        j = pygame.joystick.Joystick(0) if (len(joysticks) > 0) else MockJoystick()
        hat = j.get_hat(0)
        axisLR = j.get_axis(0)
        axisUD = j.get_axis(1)

        # player movement input
        if hat[0] == -1 or axisLR < -0.5 or keys[pygame.K_LEFT]: #left
            pass
        elif hat[0] == 1 or axisLR > 0.5 or keys[pygame.K_RIGHT]: #right
            pass
        else:
            pass
        if hat[1] == 1 or axisUD < -0.5 or keys[pygame.K_UP]: #up
            self.move_selection_up()
        elif hat[1] == -1 or axisUD > 0.5 or keys[pygame.K_DOWN]: #down
            self.move_selection_down()
        else:
            pass
            
        # menu, ok, cancel 
        if j.get_button(self.game.controller_map.controls['MENU']) or keys[pygame.K_e]:
            self.close()
        elif j.get_button(self.game.controller_map.controls['OK']) or keys[pygame.K_SPACE]:
            self.activateHighlightedOption()
        elif j.get_button(self.game.controller_map.controls['CANCEL']) or keys[pygame.K_RETURN]:
            self.close()


    def draw(self):
        self.game.states.element_before(self).draw() # draw game behind menu
        # draw menu here
        self.menu_rect.draw()

        for index, opt in enumerate(self.options.keys()):
            txt_surface = self.font.render(opt, False, TEXT_COLOR)
            rect = txt_surface.get_rect(midtop = self.menu_rect.rect.midtop + pygame.math.Vector2(0,index * TILESIZE * SCALE_FACTOR))
            self.display_surface.blit(txt_surface, rect)

            if self.selection_index == index:
                # place cursors
                self.cursorL.rect.y = rect.y
                self.cursorL.rect.x = rect.x - TILESIZE * SCALE_FACTOR * 1.5
                
                self.cursorR.rect.y = rect.y
                self.cursorR.rect.right = rect.right + TILESIZE * SCALE_FACTOR * 1.5

        self.display_surface.blit(self.cursorL.image, self.cursorL.rect)
        self.display_surface.blit(self.cursorR.image, self.cursorR.rect)


    def run(self):
        self.draw()
        self.input()
        self.cursorL.update()
        self.cursorR.update()
        self.selection_cooldown()
        self.activation_cooldown()
