import pygame


class Keyboard:
    def __init__(self):
        pygame.init()
        win = pygame.display.set_mode((100, 100))

    def get_key(self, key_name: str):
        key_pressed = False
        for event in pygame.event.get():
            pass
        key_input = pygame.key.get_pressed()
        key = getattr(pygame, 'K_{}'.format(key_name))
        if key_input[key]:
            key_pressed = True
        pygame.display.update()
        return key_pressed

    def get_multiple_keys(self, key_names: list):
        num_pressed = 0
        key_pressed = False
        for key in key_names:
            if self.get_key(key):
                num_pressed += 1
        if len(key_names) == num_pressed:
            key_pressed = True
        return key_pressed

    def arrow_control(self):
        data = None
        if self.get_multiple_keys(['RIGHT', 'UP']):
            data = '1,20,100'
        elif self.get_multiple_keys(['LEFT', 'UP']):
            data = '1,-20,100'
        elif self.get_multiple_keys(['LEFT', 'DOWN']):
            data = '-1,-20,100'
        elif self.get_multiple_keys(['RIGHT', 'DOWN']):
            data = '-1,20,100'
        elif self.get_key('UP'):
            data = '1,0,100'
        elif self.get_key('DOWN'):
            data = '-1,0,100'
        elif self.get_key('RIGHT'):
            data = '1,90,100'
        elif self.get_key('LEFT'):
            data = '1,-90,100'
        return data

    def key_q(self):

        return self.get_key('q')

    def user_input(self):
        val = input("Enter your value: ")
        return val
