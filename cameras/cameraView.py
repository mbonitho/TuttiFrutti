import pygame
from cameras.cop import Cop
from cameras.tenant import Tenant


class CameraView:

    def __init__(self, tenant_type, room_name):
        
        self.display_surface = pygame.display.get_surface()

        self.tenant = Tenant(tenant_type, (200,200))

        bg_image = pygame.image.load(f'./graphics/rooms/{room_name}.png').convert_alpha() 
        self.background = bg_image

        self.offset = (500,100)

        self.cop = None


    def addCop(self):
        self.cop = Cop('police1', self)


    def draw(self):
        # draw background
        self.display_surface.blit(self.background, self.offset)   

        # draw tenant
        if self.tenant != None:
            self.display_surface.blit(self.tenant.image, (self.tenant.rect.x + self.offset[0], self.tenant.rect.y + self.offset[1]))

        # draw cop if necessary
        if self.cop != None:
            self.display_surface.blit(self.cop.image, (self.cop.rect.x + self.offset[0], self.cop.rect.y + self.offset[1]))


    def update(self):
        if self.tenant != None:
            self.tenant.update()

        if self.cop != None:
            self.cop.update()
