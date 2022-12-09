import math
import pygame

def get_distance(rect1, rect2):
    return math.sqrt((rect2.x - rect1.x)**2 + (rect2.y - rect1.y)**2)


def get_wave_value():
    value = math.sin(pygame.time.get_ticks())
    return 255 if value > 0 else 0


def reflect_image(frame):
    return pygame.transform.flip(frame, flip_x= True, flip_y= False)


def toggle_fullscreen():
    screen = pygame.display.get_surface()
    tmp = screen.convert()
    caption = pygame.display.get_caption()
    cursor = pygame.mouse.get_cursor()  # Duoas 16-04-2007 
    
    w,h = screen.get_width(),screen.get_height()
    flags = screen.get_flags()
    bits = screen.get_bitsize()
    
    pygame.display.quit()
    pygame.display.init()
    
    screen = pygame.display.set_mode((w,h),flags+pygame.FULLSCREEN,bits)
    screen.blit(tmp,(0,0))
    pygame.display.set_caption(*caption)

    pygame.key.set_mods(0) #HACK: work-a-round for a SDL bug??

    pygame.mouse.set_cursor( *cursor )  # Duoas 16-04-2007
    
    return screen


def get_distance_direction(checker, checked):     
    
    my_vec = pygame.math.Vector2(checker.rect.center)
    player_vec = pygame.math.Vector2(checked.rect.center)

    distance = (player_vec - my_vec).magnitude()

    if distance > 0:
        direction = (player_vec - my_vec).normalize() * checker.speed
    else:
        direction = pygame.math.Vector2()
        
    return distance, direction
    