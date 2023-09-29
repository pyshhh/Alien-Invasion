import sys
import pygame
from time import sleep

from setting import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from buttons import Buttons
from scoreboard import Scoreboard


class Alien_invasion: 

    '''an overall class to  manage game assets and behvaiour'''

    def __init__(self) -> None:
        pygame.init()
        self.setting = Settings()
        self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.setting.screen_width = self.screen.get_rect().width
        self.setting.screen_height = self.screen.get_rect().height
        self.bullet = pygame.sprite.Group()


        #self.screen = pygame.display.set_mode((1200,800))
        pygame.display.set_caption("Alien Invasion")
        
        #create an instance to score the game statistics and create a scoreboard
        #create an instance to store game stats
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        
        self.ship = Ship(self)
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        self.play_button  = Buttons(self, "PLAY(P)")
        


    def run_game(self):
        '''start the main loop for the game'''
        
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self.update_bullets() 
                self._update_aliens()
            self._update_screen()
            
    
            #watch for keyboard and mouse event.
    def _check_events(self):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                 self._check_keydown(event)
            elif event.type == pygame.KEYUP:
                 self._check_keyup(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
    

    def _check_play_button(self, mouse_pos):
        """start a new game when player clicks play button"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
    
        if button_clicked and not self.stats.game_active:
            #reset the game setting
            self.setting.init_dynamics_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            #get rid of remaining bullets
            self.aliens.empty()
            self.bullet.empty()

            #create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()
            
            #hide the mouse cursor
            pygame.mouse.set_visible(False)

            #reset the game setting
            self.setting.init_dynamics_settings()
            

    def _check_keydown(self,event):
        if event.key == pygame.K_RIGHT:
         #MOVE THE SHIP TO THE RIGHT 
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
        #MOVING SHIP TO THE LEFT
            self.ship.moving_left = True

        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p:
            self.stats.game_active = True
            pygame.mouse.set_visible(False)
            
             
    def _check_keyup(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False

        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        if len(self.bullet) < self.setting.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullet.add(new_bullet)

    def update_bullets(self):
        self.bullet.update()
        for bullets in self.bullet.copy(): 
             if bullets.rect.bottom <= 0:
                self.bullet.remove(bullets)
                
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullet,self.aliens, True,True)
        if not self.aliens:
            self.bullet.empty()
            self._create_fleet()
            self.setting.increase_speed()

            #increase level
            self.stats.level += 1
            self.sb.prep_level()

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.setting.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
            

    def _create_fleet(self):
        '''a method to generate aliens'''
        alien = Alien(self)
        alien_width = alien.rect.width
       
        available_space_x = self.setting.screen_width - (2*alien_width)
        number_aliens_x = available_space_x // (2*alien_width)
        alien_width, alien_height = alien.rect.size

        ship_height = self.ship.rect.height
        availabe_space_y = (self.setting.screen_height - (3*alien_height) - ship_height)
        number_rows = availabe_space_y //(2*alien_height)

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)
           

    def _create_alien(self,alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        """update the positions of all alien in the fleet"""
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_alien_bottom()

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.setting.fleet_drop_speed
        self.setting.fleet_direction *= -1

    def _ship_hit(self):
        """respond to the ship being hit by the alien"""
        #decrement the ships_left
        if self.stats.ships_left > 0:
            #decrement ships_left, and update scoreboard   
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            #get rid of my remaining aliens and bullets.

            self.aliens.empty()
            self.bullet.empty()

            #create the new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            #pause
            sleep(0.5)
        
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
            



    def _check_alien_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break
    
    

    
 
        

    #redraw the screen during each pass through the screen
    def _update_screen(self):
        self.screen.blit(self.setting.bg_image,(0,0))
        #self.screen.fill(self.setting.bg_color)#self.bg_color = (0,0,0)
        self.ship.blitme()
        for bullet in self.bullet.sprites():
             bullet.draw_bullet()
        self.aliens.draw(self.screen)

        #DRAW THE SCORE INFORMATION
        self.sb.show_score()

        if not self.stats.game_active:
            self.play_button.draw_button()
        #may the most recently drawn screen visible
        pygame.display.flip()

if __name__ == '__main__':
        # make a game instance, and run the game.
    ai = Alien_invasion()
    ai.run_game()

