import pygame
from entities.entity import Entity
from settings import *

class Tenant(Entity):

    def __init__(self, type: str, pos: tuple):
        super().__init__()

        image = pygame.image.load(f'./graphics/{type}.png').convert_alpha()
        rect = image.get_rect()
        self.image = pygame.transform.scale(image, (int(rect.width * SCALE_FACTOR), int(rect.height * SCALE_FACTOR)))
        self.rect = self.image.get_rect(topleft = pos)

        # movement
        self.canMove = True

        # status
        self.activation_cooldown_time = 600
        self.activated_time = pygame.time.get_ticks() - self.activation_cooldown_time * 2
        self.idle = True


    def animation_cooldown(self):
        now = pygame.time.get_ticks()
        if not self.idle and  now - self.activated_time >= self.activation_cooldown_time:
            self.setImage(self.img_idle)        
            self.idle = True


    def activate(self):
        if self.idle:
            self.setImage(self.img_activated)  
            self.activated_time = pygame.time.get_ticks() 
            self.idle = False


    def update(self):
        self.animation_cooldown()
        