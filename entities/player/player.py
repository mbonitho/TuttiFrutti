import pygame
from entities.player.playerInfo import PlayerInfo
from entities.entity import Entity
from settings import *

class Player(Entity):

    def __init__(self, pos: tuple):
        super().__init__()

        self.img_idle = './graphics/heros.png'
        self.img_activated = './graphics/heros_bras_leve.png'

        self.setImage(self.img_idle)
        self.rect = self.image.get_rect(topleft = pos)

        # movement
        self.canMove = True

        # stats
        self.player_info = PlayerInfo()

        # status
        self.activation_cooldown_time = 600
        self.activated_time = pygame.time.get_ticks() - self.activation_cooldown_time * 2
        self.idle = True


    def setImage(self, img):
        image = pygame.image.load(img).convert_alpha()
        rect = image.get_rect()
        self.image = pygame.transform.scale(image, (int(rect.width * SCALE_FACTOR), int(rect.height * SCALE_FACTOR)))


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
        