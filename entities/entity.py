import pygame
from utils.miscellaneous import get_distance_direction

class Entity(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.frame_index = 0
        self.animation_speed = 0.05
        self.direction = pygame.math.Vector2()

        # invicibility timer
        self.vulnerable = True
        self.invicibility_cooldown = 175
        self.hit_time = pygame.time.get_ticks() - self.invicibility_cooldown    

        self.speed = 0


    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.rect.x += self.direction.x * speed


    def touches(self, sprite): 
        return self.rect.colliderect(sprite.rect.inflate(2,2))
