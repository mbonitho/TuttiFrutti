import pygame
from config.settings import *
from sprites.cursor import Cursor
from states.state import State
from utils.mockJoystick import MockJoystick


class TextChoiceState(State):

    def __init__(self, game, rect, npc):

        super().__init__(game)

        self.npc = npc
        # build dictionary (choice options)
        dict = {}
        for index, child_node in enumerate(npc.event_tree.parent.children):
            dict[child_node.str_message] = index
        self.choices = dict

        # General setup
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE * SCALE_FACTOR)

        # Selection system
        self.selection_cooldown_time = 300
        self.selection_index = 0
        self.selection_time = pygame.time.get_ticks() - 1000
        self.can_move_selection = True
        self.cursorL = Cursor()
        self.cursorR = Cursor()

        # activation system
        self.activation_cooldown_time = 300
        self.activation_time = pygame.time.get_ticks() + 500
        self.can_activate_choice = False
        
        # dimensions
        self.rect = rect

        # todo
        self.result_node = None


    def activateHighlightedChoice(self):
        if self.can_activate_choice:
            choice = list(self.choices.keys())[self.selection_index]
            self.can_activate_choice = False
            self.activation_time = pygame.time.get_ticks()
            for e in self.npc.event_tree.get_siblings():
                msg = list(self.choices.keys())[self.selection_index]
                if e.str_message == msg:
                    self.npc.event_tree = e.children[0]
                    self.game.states.pop()
                    # self.game.states.force_push(TextBoxState(self.game, pygame.Rect(MESSAGE_BOX_X, MESSAGE_BOX_Y, MESSAGE_BOX_WIDTH, MESSAGE_BOX_HEIGHT), self.npc))
                    break
                

    def move_selection_up(self):
        if self.can_move_selection:
            self.selection_index -= 1
            if self.selection_index < 0:
                self.selection_index = len(self.choices) - 1
            self.can_move_selection = False
            self.selection_time = pygame.time.get_ticks()


    def move_selection_down(self):
        if self.can_move_selection:
            self.selection_index += 1
            if self.selection_index > len(self.choices) - 1:
                self.selection_index = 0
            self.can_move_selection = False
            self.selection_time = pygame.time.get_ticks()


    def selection_cooldown(self):
        if not self.can_move_selection and pygame.time.get_ticks() - self.selection_time > self.selection_cooldown_time:
            self.can_move_selection = True


    def activation_cooldown(self):
        if not self.can_activate_choice and pygame.time.get_ticks() - self.activation_time > self.activation_cooldown_time:
            self.can_activate_choice = True


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
            self.activateHighlightedChoice()
            self.close()
        elif j.get_button(self.game.controller_map.controls['OK']) or keys[pygame.K_SPACE]:
            self.activateHighlightedChoice()
            self.close()
        elif j.get_button(self.game.controller_map.controls['CANCEL']) or keys[pygame.K_RETURN]:
            self.activateHighlightedChoice()
            self.close()


    def draw(self):
        self.game.states.element_before(self).draw() # draw previous state behind choice
        
        # draw item list here
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, self.rect)

        for index, opt in enumerate(self.choices):
            txt_surface = self.font.render(f'{opt}', False, TEXT_COLOR)
            rect = txt_surface.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(UI_FONT_SIZE * .25, UI_FONT_SIZE * .25 + index * 20))
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
