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


    def __init__(self, tenant_type, room_name, display_message):
        
        self.get_arrestation_consequences = display_message

        self.display_surface = pygame.display.get_surface()

        self.tenant = Tenant(tenant_type, (self.TENANT_STARTX, self.TENANT_STARTY))
        self.visitors = []

        bg_image = pygame.image.load(f'./graphics/rooms/{room_name}.png').convert_alpha() 
        self.background = bg_image

        self.offset = (175,70)

        self.cop = None

        # infractions
        self.is_illegal = False
        self.illegal_cooldown_time = BAD_BEHAVIOR_DURATION
        self.illegal_start_time = pygame.time.get_ticks() - self.illegal_cooldown_time * 2

        self.status = 'normal'


    def illegal_cooldown(self):
        now = pygame.time.get_ticks()
        if self.is_illegal and  now - self.illegal_start_time >= self.illegal_cooldown_time:
            self.is_illegal = False
            self.status = 'normal'
            self.visitors = []


    def setBadBehavior(self, law_code, time):

        self.illegal_start_time = pygame.time.get_ticks() 
        self.is_illegal = True

        if law_code == LAW_NO_MUSIC:
            self.status = 'singing'
        elif law_code == LAW_NO_OPENED_WINDOW:
            self.status = 'openedWindow'
        elif law_code == LAW_LIGHTS_ALWAYS_ON:
            self.status = 'lights_off'
        elif law_code == LAW_DONT_STOP_MOVING:
            self.status = 'stopped'
        elif law_code == LAW_NO_VISIT_OTHER_SPECIES:
            self.addVisitorDifferentSpecies()
        elif law_code == LAW_NO_VISIT_SAME_SPECIES:
            self.addVisitorSameSpecies()


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

        # opened window
        if self.status == 'openedWindow':
            pygame.draw.rect(self.display_surface, 'blue', self.background.get_rect().inflate(-50,-50))

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

            # new tenant
            name = choice(CameraView.tenant_types)

            # reward or penalize
            self.get_arrestation_consequences(self.is_illegal)

            self.tenant = Tenant(name, (self.TENANT_STARTX, self.TENANT_STARTY))
            self.status = 'normal'
            self.is_illegal = False

        self.illegal_cooldown()