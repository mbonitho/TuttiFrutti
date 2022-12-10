import pygame
from cameras.tenant import Tenant


class CameraView:

    def __init__(self, tenant_type, room_name):
        
        self.display_surface = pygame.display.get_surface()

        self.tenant = Tenant(tenant_type, (0,0)) # todo random

        bg_image = pygame.image.load(f'./graphics/rooms/{room_name}.png').convert_alpha() # todo random
        self.background = bg_image

        self.offset = (500,100)


    def draw(self):
        # draw background
        self.display_surface.blit(self.background, self.offset)   

        # draw tenant
        self.display_surface.blit(self.tenant.image, (self.tenant.rect.x + self.offset[0], self.tenant.rect.y + self.offset[1]))


    def update(self):
        pass