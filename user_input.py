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

    def user_input(self):
        val = input("Enter your value: ")
        return val
