import pygame
import time
import sys


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


class Joystick:
    def __init__(self):
        pygame.init()
        # control number
        try:
            self.controller = pygame.joystick.Joystick(0)
            self.controller.init()
        except pygame.error as error:
            print('Joystick not connected')
            print(error)
            sys.exit(1)

        self.button = {'x': 0, 'o': 0, 't': 0, 's': 0, 'L1': 0, 'R1': 0, 'L2': 0,
                       'R2': 0, 'axis1': 0., 'axis2': 0., 'axis3': 0., 'axis4': 0.}
        self.axiss = [0., 0., 0., 0., 0., 0.]

    def getJS(self, name=''):

        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                self.axiss[event.axis] = round(event.value, 2)
            elif event.type == pygame.JOYBUTTONDOWN:
                for x, (key, val) in enumerate(self.button.items()):
                    if x < 10:
                        if self.controller.get_button(x):
                            self.button[key] = 1
            elif event.type == pygame.JOYBUTTONUP:
                for x, (key, val) in enumerate(self.button.items()):
                    if x < 10:
                        if event.button == x:
                            self.button[key] = 0

        self.button['axis1'] = self.axiss[0]
        self.button['axis2'] = self.axiss[1]
        self.button['axis3'] = self.axiss[2]
        self.button['axis4'] = self.axiss[3]

        if not name:
            return self.button
        else:
            return self.button[name]
