import pygame
from settings import *
from utils.miscellaneous import reflect_image

class Cursor(pygame.sprite.Sprite):

    def __init__(self, flipped: bool = False):
        super().__init__()

        self.animation = self.import_animation(flipped)
        self.frame_index = 0
        self.animation_speed = 0.10
        self.image = self.animation[0]
        self.rect = self.image.get_rect()


    def import_animation(self, flipped: bool ):
            c1 = pygame.image.load('./graphics/curseur/curseur1.png').convert_alpha()
            c2 = pygame.image.load('./graphics/curseur/curseur2.png').convert_alpha()
            c3 = pygame.image.load('./graphics/curseur/curseur3.png').convert_alpha()

            rect = c1.get_rect()

            c1 = pygame.transform.scale(c1, (int(rect.width * SCALE_FACTOR), int(rect.height * SCALE_FACTOR)))
            c2 = pygame.transform.scale(c2, (int(rect.width * SCALE_FACTOR), int(rect.height * SCALE_FACTOR)))
            c3 = pygame.transform.scale(c3, (int(rect.width * SCALE_FACTOR), int(rect.height * SCALE_FACTOR)))

            if flipped:
                c1 = reflect_image(c1)
                c2 = reflect_image(c2)
                c3 = reflect_image(c3)

            return [c1,c2,c3]


    def animate(self):

        # increment frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animation):
            self.frame_index = 0

        # set the image
        self.image = self.animation[int(self.frame_index)]

    def update(self):
        self.animate()