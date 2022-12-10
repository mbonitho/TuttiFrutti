import pygame
from cameras.tenant import Tenant


class CameraView:

    def __init__(self):
        
        self.display_surface = pygame.display.get_surface()

        self.tenant = Tenant('locataire', (0,0)) # todo random

        bg_image = pygame.image.load('./graphics/salon.png').convert_alpha() # todo random
        self.background = bg_image

        self.offset = (500,100)


    def draw(self):
        # draw background
        self.display_surface.blit(self.background, self.offset)   

        # draw tenant
        self.display_surface.blit(self.tenant.image, (self.tenant.rect.x + self.offset[0], self.tenant.rect.y + self.offset[1]))


    def update(self):
        pass