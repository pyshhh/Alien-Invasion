import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard:

    def __init__(self,ai_game) -> None:

        """initalize scorkeeping attribute"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.setting = ai_game.setting
        self.stats = ai_game.stats

        #font setting for scoring information
        self.text_color = (225,225,225)
        self.font = pygame.font.SysFont(None,48)
         
        #prepare the inital score image
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    
    def prep_score(self):
        '''truns the score into a rendered image'''
        rounded_score = round(self.stats.score,-1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str,True,self.text_color,self.setting.bg_color)


        #display the score at top right cornor
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """draw scores,ships and level to the screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.prep_high_score_image,self.high_score_rect)
        self.screen.blit(self.level_image,self.level_rect)
        self.ships.draw(self.screen)


    
    def prep_high_score(self):
        """turn the high score into a rendered image"""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.prep_high_score_image = self.font.render(high_score_str,True,self.text_color,self.setting.bg_color)

        #center the high score at the top of the screen.
        self.high_score_rect = self.prep_high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.screen_rect.top


    def check_high_score(self):
        """check to see if there is any new highscore"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()


    def prep_level(self):
        """turn the level into a rendered image"""
        level_str = str(self.stats.level)
        self.level_image  =  self.font.render(level_str,True,self.text_color,self.setting.bg_color)

        #position the level below the score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """showe how many ships are left"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

        