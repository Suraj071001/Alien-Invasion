import pygame.font
from pygame.sprite import Group

from ship import Ship


class Scoreboard:
    """A class to report scoring information."""

    def __init__(self,ai_settings, screen, stats):
        """Initialize scorekeeping attributes."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # initialise the color and font of score
        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None,24)

        # prepare the first image of score
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ship()

    def prep_score(self):
        """initialise the first image of score"""
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color,self.ai_settings.bg_color)

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """Draw score to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image,self.high_score_rect)
        self.screen.blit(self.game_level_image,self.game_level_rect)
        # draw ship
        self.ships.draw(self.screen)

    def prep_high_score(self):
        round_high_score = int(round(self.stats.high_score,-1))
        high_score_str = "{:,}".format(round_high_score)
        self.high_score_image = self.font.render(high_score_str,True,self.text_color,self.ai_settings.bg_color)

        #display the first image of high score
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.top = self.screen_rect.top + 20
        self.high_score_rect.centerx = self.screen_rect.centerx

    def prep_level(self):
        level = str(self.stats.game_level)
        self.game_level_image = self.font.render(level,True,self.text_color,self.ai_settings.bg_color)

        #display the level
        self.game_level_rect = self.game_level_image.get_rect()
        self.game_level_rect.right = self.score_rect.right
        self.game_level_rect.top = self.score_rect.top + 20 + self.score_rect.height

    def prep_ship(self):
        """show no. of ships on screen """
        self.ships = Group()
        for number_ship in range(self.stats.ships_left) :
            ship = Ship(self.ai_settings,self.screen)
            ship.rect.x = 10 + ship.rect.width * number_ship
            ship.rect.y =10
            self.ships.add(ship)



