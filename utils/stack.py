import pygame

class Stack(): 

    def __init__(self):
        self.elements = []


    def peek(self):
        if len(self.elements) > 0:
            return self.elements[len(self.elements) - 1][1]
        else:
            return None


    def pop(self):
        return self.elements.pop()


    def element_before(self, item):
        
        element = None
        for e in self.elements:
            if e[1] == item:
                element = e
                break
        if element == None or e[0] == 1:
            return None

        return self.elements[element[0] - 2][1]


    def push(self, item):
        position_in_stack = len(self.elements) + 1
        self.elements.append((position_in_stack, item))


    def size(self):
        return len(self.elements)


    def empty(self):
        return len(self.elements) > 0


    def clear(self):
        self.elements = []


class TimedStack(Stack):

    def __init__(self, time = 500):
        super().__init__()
        self.time = time
        self.last_change_time = pygame.time.get_ticks() - self.time * 2


    def push(self, item):
        if pygame.time.get_ticks() - self.last_change_time > self.time:
            super().push(item)
            self.last_change_time = pygame.time.get_ticks()


    def force_push(self, item):
        super().push(item)
        self.last_change_time = pygame.time.get_ticks()
        

    def pop(self):
        if pygame.time.get_ticks() - self.last_change_time > self.time:
            super().pop()
            self.last_change_time = pygame.time.get_ticks()


    def force_pop(self):
        super().pop()
        self.last_change_time = pygame.time.get_ticks()
