import pygame
from config.settings import *
from sprites.cursor import Cursor
from states.state import State
from theming.themedRect import ThemedRect
from utils.mockJoystick import MockJoystick


class TextBoxState(State):

    def __init__(self, game, npc):
        
        super().__init__(game)

        self.npc = npc

        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE * SCALE_FACTOR)
        
        self.current_letter_index = 0
        self.text_speed = TEXT_SPEED
        self.previous_letter_time = pygame.time.get_ticks() - 1000

        self.advance_text_cooldown_time = 300
        self.advance_text_index = 0
        self.advance_text_time = pygame.time.get_ticks() - 1000
        self.can_advance_text = True

        # General setup
        self.lines = self.get_lines(npc.event_tree.str_message)

        # dimensions
        screen_width = pygame.display.get_surface().get_width()
        screen_height = pygame.display.get_surface().get_height()
        rect = pygame.Rect( screen_width * 0.05, 
                           screen_height * 0.75, 
                           screen_width * 0.9, 
                           screen_height * 0.2)
        self.boxRect = ThemedRect(rect)

        # Cursor
        self.cursor = Cursor()
        self.cursor.rect.bottomright = rect.bottomright


    def get_lines(self, text):
        lines = []
        words = text.split(' ')
        curr_line = ''
        for i in range(0, len(words)):
            current_word = words[i]
            next_word = '' if i == len(words) -1 else words[i+1]
            curr_line += f'{current_word} ' 
            if len(f'{curr_line} {next_word}'.strip()) > MAX_CHAR_PER_LINE or next_word == '':
                lines.append(curr_line)
                curr_line = ''
        self.current_line_index = 0
        return lines


    def advanceLetters(self):
        self.current_letter_index = min(self.current_letter_index + self.text_speed, 
                                len(self.lines[self.current_line_index]) - 1)


    def advance_text(self):
        if self.can_advance_text:

            self.can_advance_text = False
            self.advance_text_time = pygame.time.get_ticks()

            if self.current_letter_index < len(self.lines[self.current_line_index]) - 1:
                self.current_letter_index = len(self.lines[self.current_line_index]) - 1
                return

            if self.current_line_index < len(self.lines) - 1:
                self.current_line_index += 1
                self.current_letter_index = 0
            else:
                self.game.states.pop()


    def advance_text_cooldown(self):
        if not self.can_advance_text and pygame.time.get_ticks() - self.advance_text_time > self.advance_text_cooldown_time:
            self.can_advance_text = True


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
            pass
        elif hat[1] == -1 or axisUD > 0.5 or keys[pygame.K_DOWN]: #down
            pass
        else:
            pass
            
        # menu, ok, cancel 
        if j.get_button(self.game.controller_map.controls['MENU']) or keys[pygame.K_e]:
            self.advance_text()
        elif j.get_button(self.game.controller_map.controls['OK']) or keys[pygame.K_SPACE]:
            self.advance_text() 
        elif j.get_button(self.game.controller_map.controls['CANCEL']) or keys[pygame.K_RETURN]:
            self.advance_text() 


    def draw(self):
        self.game.states.element_before(self).draw() 
        

        self.boxRect.draw()

        text_to_render = self.lines[self.current_line_index][0:int(self.current_letter_index)]
        txt_surface = self.font.render(text_to_render, False, TEXT_COLOR)
        rect = txt_surface.get_rect(midtop = self.boxRect.rect.midtop + pygame.math.Vector2(0, UI_FONT_SIZE * .25))
        self.display_surface.blit(txt_surface, rect)

        if self.current_letter_index == len(self.lines[self.current_line_index]) - 1:
            self.display_surface.blit(self.cursor.image, self.cursor.rect)


    def run(self):
        self.draw()
        self.input()
        self.advanceLetters()
        self.advance_text_cooldown()
        self.cursor.update()
