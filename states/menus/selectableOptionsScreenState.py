import pygame
from settings import *
from sprites.cursor import Cursor
from states.state import State
from theming.themedRect import ThemedRect


class SelectableOptionsScreenState(State):

    def __init__(self, game, has_themed_box = False):
        super().__init__(game)

        self.font = pygame.font.Font(UI_FONT, int(UI_FONT_SIZE * SCALE_FACTOR))

        # Selection system
        self.selection_cooldown_time = 300
        self.selection_index = 0
        self.selection_time = pygame.time.get_ticks() - 1000
        self.can_move_selection = True
        self.cursorL = Cursor()
        self.cursorR = Cursor(flipped=True)
        
        self.rect = self.display_surface.get_rect()

        # activation system
        self.activation_cooldown_time = 300
        self.activation_time = pygame.time.get_ticks() + 500
        self.can_activate_selection = False

        self.has_themed_box = has_themed_box


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


    def activateHighlightedOption(self):
        if self.can_activate_selection:
            option_name = list(self.options.keys())[self.selection_index]
            action_to_perform = self.options[option_name]
            action_to_perform()
            self.can_activate_selection = False
            self.activation_time = pygame.time.get_ticks()


    def input(self):

        keys = pygame.key.get_pressed()
        # player movement input
        if keys[pygame.K_LEFT]: #left
            pass
        elif keys[pygame.K_RIGHT]: #right
            pass
        else:
            pass
        if keys[pygame.K_UP]: #up
            self.move_selection_up()
        elif keys[pygame.K_DOWN]: #down
            self.move_selection_down()
        else:
            pass
            
        # menu, ok, cancel 
        if keys[pygame.K_SPACE]:
            self.activateHighlightedOption()
        elif keys[pygame.K_RETURN]:
            self.activateHighlightedOption()


    def draw(self):
        self.display_surface.fill('gray')

        # Themed box around options
        if self.has_themed_box:
            width = self.getMaxTextWidth() + MARGIN * SCALE_FACTOR * 2
            height = len(self.options) * UI_FONT_SIZE * SCALE_FACTOR + MARGIN * SCALE_FACTOR * 2
            left = self.display_surface.get_width() / 2 - width / 2
            top =  HEIGHT * 0.6 -MARGIN * SCALE_FACTOR
            rect = pygame.rect.Rect(left, top, width, height).inflate(self.cursorL.rect.width  * 2,  MARGIN * SCALE_FACTOR / 2)
            ThemedRect(rect).draw()
            
        # options
        for index, opt in enumerate(self.options.keys()):
            txt_surface = self.font.render(opt, False, TEXT_COLOR)
            rect = txt_surface.get_rect(midtop = (self.display_surface.get_width() / 2, HEIGHT * 0.6) + pygame.math.Vector2(0, index * UI_FONT_SIZE * SCALE_FACTOR))
            self.display_surface.blit(txt_surface, rect)
            if self.selection_index == index:
                # place cursors
                self.cursorL.rect.y = rect.y
                self.cursorL.rect.right = rect.x - MARGIN * SCALE_FACTOR * 1.5
                
                self.cursorR.rect.y = rect.y
                self.cursorR.rect.left = rect.right + MARGIN * SCALE_FACTOR * 1.5

        self.display_surface.blit(self.cursorL.image, self.cursorL.rect)
        self.display_surface.blit(self.cursorR.image, self.cursorR.rect)


    def getMaxTextWidth(self):
        max = 0
        for text in self.options.keys():
            txt_surface = self.font.render(text, False, TEXT_COLOR)
            rect = txt_surface.get_rect()
            if rect.width > max:
                max = rect.width
        return max


    def run(self):
        self.draw()
        self.input()
        self.activation_cooldown()
        self.selection_cooldown()
        self.cursorL.update()
        self.cursorR.update()
        