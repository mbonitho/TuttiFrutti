import pygame
from settings import *
from entities.player.player import Player
from states.state import State
from utils.miscellaneous import is_near_enough
from cameras.cameraView import CameraView

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

    def cameras_setup(self):
        for i in range(NUMBER_OF_CAMERAS):
            cv = CameraView()
            self.cameras.append(cv)


    def activation_cooldown(self):
        if not self.can_activate_selection and pygame.time.get_ticks() - self.activation_time > self.activation_cooldown_time:
            self.can_activate_selection = True


    def activatePlayer(self):
        self.player.activate()
        
        if self.can_activate_selection:

            for location in [POLICE_BUTTON_X, CAM_BUTTON_X, PAPERS_X]:

                if is_near_enough(location, self.player.rect.x, 50):
                    print(location)

                    self.can_activate_selection = False
                    self.activation_time = pygame.time.get_ticks()


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


    def run(self):
        self.draw()
        self.player.update()
        self.activation_cooldown()
        self.update_cameras_views()
