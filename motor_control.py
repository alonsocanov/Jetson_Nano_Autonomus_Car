import pygame


def user_input():
    val = input("Enter your value: ")
    return val


def initInpuWindow():
    pygame.init()
    win = pygame.display.set_mode((100, 100))


def get_key(key_name):
    key_pressed = False
    for event in pygame.event.get():
        pass
    key_input = pygame.key.get_pressed()
    key = getattr(pygame, 'K_{}'.format(key_name))
    if key_input[key]:
        key_pressed = True
    pygame.display.update()
    return key_pressed
