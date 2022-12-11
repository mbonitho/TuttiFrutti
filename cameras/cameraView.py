import pygame
from cameras.cop import Cop
from cameras.tenant import Tenant
from settings import *
from random import choice, randint

class CameraView:

    room_types = ['salon1', 'salon2', 'salon3', 'salon4']
    tenant_types = ['ben', 'clement', 'tommy', 'ted', 'paula', 'peach']

    TENANT_STARTX = 200
    TENANT_STARTY = 160

    def __init__(self, tenant_type, room_name, consequences):
        
        self.get_arrestation_consequences = consequences

        self.display_surface = pygame.display.get_surface()

        self.tenant = Tenant(tenant_type, (self.TENANT_STARTX, self.TENANT_STARTY))
        self.visitors = []

        bg_image = pygame.image.load(f'./graphics/rooms/{room_name}.png').convert_alpha() 
        self.background = bg_image
        self.curtains_open_image = pygame.image.load(f'./graphics/rooms/rideaux_ouverts.png').convert_alpha() 
        self.curtains_open_rect = self.curtains_open_image.get_rect(topleft= (180,0)) 
        self.curtains_closed_image = pygame.image.load(f'./graphics/rooms/rideaux_fermes.png').convert_alpha() 
        self.curtains_closed_rect = self.curtains_open_image.get_rect(topleft= (100,0)) 

        self.offset = (175,70)

        self.cop = None

        # infractions
        self.is_illegal = False
        self.behavior_cooldown_time = BEHAVIOR_DURATION
        self.behavior_start_time = pygame.time.get_ticks() - self.behavior_cooldown_time * 2

        self.status = 'normal'


    def behavior_cooldown(self):
        now = pygame.time.get_ticks()
        if not self.status == 'cop' and self.is_illegal and  now - self.behavior_start_time >= self.behavior_cooldown_time:
            self.is_illegal = False
            self.status = 'normal'
            self.visitors = []


    def setBehavior(self, law_code: int, is_illegal: bool):

        self.behavior_start_time = pygame.time.get_ticks() 
        self.is_illegal = is_illegal

        if law_code == LAW_NO_MUSIC:
            self.status = 'singing'
        elif law_code == LAW_NO_OPENED_CURTAINS:
            self.status = 'closed_curtains'
        elif law_code == LAW_LIGHTS_ALWAYS_ON:
            self.status = 'lights_off'
        elif law_code == LAW_DONT_STOP_MOVING:
            self.status = 'stopped'
        elif law_code == LAW_NO_VISIT_OTHER_SPECIES:
            self.addVisitorDifferentSpecies()
        elif law_code == LAW_NO_VISIT_SAME_SPECIES:
            self.addVisitorSameSpecies()
        elif law_code == NO_MULTIPLE_VISITORS:
            for _ in range(randint(2,3)):
                self.addVisitorDifferentSpecies()


    def addVisitorSameSpecies(self):
        x = randint(self.tenant.rect.x - 50, self.tenant.rect.x + 50)
        visitor = Tenant(self.tenant.name, (x, self.tenant.rect.y))
        self.visitors.append(visitor)


    def addVisitorDifferentSpecies(self):
        candidates = CameraView.tenant_types.copy()
        candidates.remove(self.tenant.name)
        name = choice(candidates)
        x = randint(self.tenant.rect.x - 50, self.tenant.rect.x + 50)
        visitor = Tenant(name, (x, self.tenant.rect.y))
        self.visitors.append(visitor)


    def addCop(self):
        self.status = 'cop'
        self.cop = Cop(self)
        self.visitors = []


    def draw(self):
        # draw background
        self.display_surface.blit(self.background, self.offset)   

        # draw visitors
        for visitor in self.visitors:
            self.display_surface.blit(visitor.image, (visitor.rect.x + self.offset[0], visitor.rect.y + self.offset[1]))

        # draw tenant
        if self.tenant != None:
            self.display_surface.blit(self.tenant.image, (self.tenant.rect.x + self.offset[0], self.tenant.rect.y + self.offset[1]))

        # closed curtains
        if self.status == 'closed_curtains':
            self.display_surface.blit(self.curtains_closed_image, (self.curtains_closed_rect.x + self.offset[0], self.curtains_closed_rect.y + self.offset[1]))
        else:
            self.display_surface.blit(self.curtains_open_image, (self.curtains_open_rect.x + self.offset[0], self.curtains_open_rect.y + self.offset[1]))

        # music if necessary
        if self.status == 'singing':
            self.display_surface.blit(self.tenant.image_music_note, (self.tenant.rect.x + self.offset[0] + 32 * self.tenant.direction[0], self.tenant.rect.top + self.offset[1]))

        # draw cop if necessary
        if self.cop != None:
            self.display_surface.blit(self.cop.image, (self.cop.rect.x + self.offset[0], self.cop.rect.y + self.offset[1]))

        # lights off if necessary
        if self.status == 'lights_off':
            pygame.draw.rect(self.display_surface, 'black', self.background.get_rect(topleft=self.offset))


    def update(self):
        if self.tenant != None:

            if self.status == 'stopped':
                self.tenant.speed = 0
            else:
                self.tenant.speed = 1

            self.tenant.update()

            for visitor in self.visitors:
                visitor.update()

            if self.tenant.rect.x > 800:
                self.tenant = None
                self.cop = None

        if self.cop != None:
            self.cop.update()    

        if self.status == 'cop' and self.cop == None:

            # reward or penalize
            self.get_arrestation_consequences(self.is_illegal)

            # new tenant
            name = choice(CameraView.tenant_types)
            self.tenant = Tenant(name, (self.TENANT_STARTX, self.TENANT_STARTY))
            self.status = 'normal'
            self.is_illegal = False

        self.behavior_cooldown()