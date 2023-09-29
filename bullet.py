
from typing import Any
import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):

    '''a class that manages the bullet'''

    def __init__(self, ai_game):
        super().__init__()

        self.screen = ai_game.screen
        self.setting = ai_game.setting
        self.color = self.setting.bullet_color

        #creating a rect at (0,0) and then set the correct psoition
        self.rect = pygame.Rect(0,0,self.setting.bullet_width,self.setting.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop


        #store the decimal value i.e, bullet's position.
        self.y = float(self.rect.y)


    def update(self):
        #moving the bullet up the screen
        self.y -= self.setting.bullet_speed
        self.rect.y = self.y#..........updating the bulet's rect position

    def draw_bullet(self):
        '''draw the bullet to the screen'''
        pygame.draw.rect(self.screen,self.color,self.rect)

    

    