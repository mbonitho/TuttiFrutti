import pygame
from settings import *
from entities.player.player import Player
from states.state import State
from utils.miscellaneous import is_near_enough
from cameras.cameraView import CameraView
from random import choice
from theming.themedRect import ThemedRect

class GameState(State):

    def __init__(self, game):

        super().__init__(game)

        self.player = Player((WIDTH / 2, HEIGHT - 400))

        bg_image = pygame.image.load('./graphics/poste_surveillance.png').convert_alpha()
        self.background = bg_image

        # activation system
        self.activation_cooldown_time = 300
        self.activation_time = pygame.time.get_ticks() + 500
        self.can_activate_selection = False

        self.camera_index = 0
        self.cameras = []
        self.cameras_setup()

        self.cops_cooldown_time = 10000
        self.cops_call_time = pygame.time.get_ticks() - 10000
        self.can_call_cops = False

        self.laws = []


        # income
        h = self.display_surface.get_height()
        w = self.display_surface.get_width()
        self.day_number = 1
        self.income_height = h * 0.1
        self.income_width = w * 0.1
        rect = pygame.Rect(w * .9, h * .9, self.income_width, self.income_height)
        self.income_box_rect = ThemedRect(rect)


    def cameras_setup(self): # TESTER L'INCREMENTATION DES CAMERAS (DANS activatePlayer AVEC CAM_BUTTON_X)
        rooms = ['cuisine', 'salon', 'chambre1', 'chambre2']
        tenants = ['poire', 'cerise', 'clementine', 'datte']
        for i in range(NUMBER_OF_CAMERAS):
            tenant = choice(tenants)
            tenants.remove(tenant)

            room = choice(rooms)
            rooms.remove(room)
            cv = CameraView(tenant,room)
            self.cameras.append(cv)


    def activation_cooldown(self):
        if not self.can_activate_selection and pygame.time.get_ticks() - self.activation_time > self.activation_cooldown_time:
            self.can_activate_selection = True


    def cops_cooldown(self):
        if not self.can_call_cops and pygame.time.get_ticks() - self.cops_call_time > self.cops_cooldown_time:
            self.can_call_cops = True


    def activatePlayer(self):
        self.player.activate()
        
        if self.can_activate_selection:

            for location in [POLICE_BUTTON_X, CAM_BUTTON_X, PAPERS_X]:

                if is_near_enough(location, self.player.rect.x, 50):

                    if location == CAM_BUTTON_X:
                        self.switch_cameras()

                    elif location == POLICE_BUTTON_X:
                        self.call_police()

                    self.can_activate_selection = False
                    self.activation_time = pygame.time.get_ticks()


    def switch_cameras(self):
        self.camera_index += 1
        if self.camera_index >= len(self.cameras):
            self.camera_index = 0

    
    def call_police(self):
        current_camera = self.cameras[self.camera_index]
        if self.can_call_cops and current_camera.tenant != None:
            self.can_call_cops = False
            current_camera.addCop()


    def playerMove(self, direction):
        if self.player.canMove:
            self.player.rect.x += direction * PLAYER_SPEED


    def update_cameras_views(self):
        for cv in self.cameras:
            cv.update()


    def input(self):
       
        keys = pygame.key.get_pressed()

        # player movement input
        if keys[pygame.K_LEFT]: #left
            self.playerMove(-1)
        elif keys[pygame.K_RIGHT]: #right
            self.playerMove(1)
        else:
            self.player.direction.x = 0

        if keys[pygame.K_SPACE]or keys[pygame.K_RETURN]: # OK
            self.activatePlayer()


    def draw(self):
        # draw current camera view
        self.cameras[self.camera_index].draw()

        # draw background
        self.display_surface.blit(self.background, (0,0))   

        # draw player
        self.display_surface.blit(self.player.image, (self.player.rect.x, self.player.rect.y))

        # draw income
        font = pygame.font.Font(UI_FONT, UI_FONT_SIZE  * SCALE_FACTOR)
        income_text_surface = font.render(f'Jour {self.day_number} | {self.player.player_info.current_income}$', False, TEXT_COLOR)
        income_text_rect = income_text_surface.get_rect(bottomright=(self.display_surface.get_width() - UI_FONT_SIZE * SCALE_FACTOR * 0.25, self.display_surface.get_height() - UI_FONT_SIZE * SCALE_FACTOR * 0.25))
        income_box_rect = pygame.rect.Rect(income_text_rect.inflate(UI_FONT_SIZE * SCALE_FACTOR * 0.25, 0))
        income_box_rect.midtop = income_text_rect.midtop
        self.income_box_rect.update_rect(income_box_rect)
        self.income_box_rect.draw()
        self.display_surface.blit(income_text_surface, income_text_rect)


    def run(self):
        self.draw()
        self.player.update()
        self.activation_cooldown()
        self.cops_cooldown()
        self.update_cameras_views()
