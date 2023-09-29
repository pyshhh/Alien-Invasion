
import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    '''a class to manage the ship'''

    def __init__(self,ai_game) -> None:
        '''initializing the ship and set its starting point'''
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.setting = ai_game.setting


    #load the ship image and get its rect
        self.image = pygame.image.load("Alien_Invasion/resources/ship.png")
        self.rect = self.image.get_rect()

    #start each new ship at the bottem center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

    #Moving Flag variable
       
        self.moving_right = False
        self.moving_left = False

    #stores a decimal value for ship's speed
        self.x = float(self.rect.x)

    def update(self):
        
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.setting.ship_speed
        
        if self.moving_left and self.rect.left > 0:
            self.x -= self.setting.ship_speed

        #update the rect object from self.x
        self.rect.x = self.x

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        


    def blitme(self):   
        """draw the ship at its current location"""
        self.screen.blit(self.image,self.rect)
        #bit() method is used to place an image on the screen
