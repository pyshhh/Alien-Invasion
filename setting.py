import pygame

class Settings:
    '''A class to store all the setting for Alien Invasion'''

    def __init__(self) -> None:
        '''initialize the game static setting'''

        #screen setting
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color =(0,0,0)#black
        self.bg_image = pygame.image.load("Alien_Invasion/resources/bg.bmp")
        
        self.ships_limit = 3

        #bullet setting
        
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (225,60,60)
        self.bullet_allowed = 4

        #alien setting
        self.fleet_drop_speed = 10

        #score setting
        self.alien_points = 1
        

        #how quick the game speeds
        self.speedup_scale = 1.1

        self.init_dynamics_settings()

    def init_dynamics_settings(self):
        '''initializing settings that change throughtout the game'''
        self.ship_speed = 10
        self.bullet_speed = 7.5
        self.alien_speed = 3.0
        #fleet direction of 1 represents right and -1 left
        self.fleet_direction = 1

    def increase_speed(self):
        '''increase the speed settings'''
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale


    

        