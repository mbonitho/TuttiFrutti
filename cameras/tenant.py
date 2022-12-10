import pygame
from entities.entity import Entity
from settings import *
from random import choice
from utils.miscellaneous import rotation_center

class Tenant(Entity):

    def __init__(self, type: str, pos: tuple):
        super().__init__()

        image_straight = pygame.image.load(f'./graphics/tenants/{type}.png').convert_alpha()
        rect_straight = image_straight.get_rect()
        self.image_straight = pygame.transform.scale(image_straight, (int(rect_straight.width * SCALE_FACTOR), int(rect_straight.height * SCALE_FACTOR)))

        image_left, rect_left = rotation_center(image_straight, -7, rect_straight.centerx, rect_straight.bottom)
        self.image_left = pygame.transform.scale(image_left, (int(rect_left.width * SCALE_FACTOR), int(rect_left.height * SCALE_FACTOR)))

        image_right, rect_right = rotation_center(image_straight, 7, rect_straight.centerx, rect_straight.bottom)
        self.image_right = pygame.transform.scale(image_right, (int(rect_right.width * SCALE_FACTOR), int(rect_right.height * SCALE_FACTOR)))

        self.image = self.image_straight
        self.rect = self.image.get_rect(topleft = pos)

        # movement
        self.canMove = True

        # status
        self.activation_cooldown_time = 600
        self.activated_time = pygame.time.get_ticks() - self.activation_cooldown_time * 2
        self.idle = True

        self.direction = pygame.math.Vector2(choice([-1, 1]), 0)
        self.speed = 1

        self.rotation_direction = 1 # -1, 0, 1
        self.rotation_angle = 0

        self.image, self.rect = rotation_center(self.image, self.rotation_angle, self.rect.centerx, self.rect.centery)


    def animation_cooldown(self):
        now = pygame.time.get_ticks()
        if not self.idle and  now - self.activated_time >= self.activation_cooldown_time:
            self.setImage(self.img_idle)        
            self.idle = True


    def move(self, speed):
        if self.canMove:
            if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize()
            self.rect.x += self.direction.x * speed
            self.rotation_angle += self.rotation_direction


    def check_turn_around(self):

        if not self.canMove:
            return

        left = 0
        if self.rect.x < left:
           self.rect.x = left 
           self.direction *= -1

        right = 600
        if self.rect.x > right:
            self.rect.x = right 
            self.direction *= -1


    def change_rotation(self):
    
        min = -22
        if self.rotation_angle < min:
            self.rotation_angle = min
            self.rotation_direction *= -1

        max = -min
        if self.rotation_angle > max:
            self.rotation_angle = max
            self.rotation_direction *= -1

        # skip frames
        if self.rotation_angle == 0:
            self.image = self.image_straight
        if self.rotation_angle == min:
            self.image = self.image_left
        if self.rotation_angle == max:
            self.image = self.image_right


    def update(self):
        self.animation_cooldown()
        self.move(self.speed)
        self.check_turn_around()
        self.change_rotation()
        