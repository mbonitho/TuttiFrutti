import pygame

class Camera():

    def __init__(self):

        # general setup
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2

        self.offset = pygame.math.Vector2()


    def draw_sprites(self, player, effects, groups): 

        # getting the offset (camera)
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing each sprite group
        for group in groups: 
            for sprite in group:
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image,offset_pos)          

        # drawing player 
        offset_pos = player.rect.topleft - self.offset
        self.display_surface.blit(player.image,offset_pos)

        # drawing effects
        for effect in effects:
            offset_pos = effect.rect.topleft - self.offset
            self.display_surface.blit(effect.image,offset_pos)    
