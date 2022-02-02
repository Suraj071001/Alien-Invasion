from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

import pygame

def run_game():
    # Initialize game and create a screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("alien_invasion")
    # Make a ship.
    ship = Ship(ai_settings,screen)
    bullets = Group()
    aliens = Group()

    # create a instance for game stats
    stats = GameStats(ai_settings)

    #instance of score
    sb = Scoreboard(ai_settings,screen,stats)

    #create the fleet aliens
    gf.create_fleet(ai_settings, screen, aliens,ship)

    #create buttons
    play_button = Button(ai_settings,screen,"Play")
    ship.update()
    gf.update_bullets(aliens, bullets, ai_settings, screen, ship, stats, sb)
    gf.update_alien(ai_settings, stats, screen, ship, aliens, bullets, sb)
    gf.update_screen(ai_settings, screen, ship, aliens, bullets, stats, play_button, sb)
    # Start the main loop for the game.
    while True:
        # Watch for keyboard and mouse events
        gf.event_check(ai_settings, screen,ship,bullets,stats,play_button,aliens,sb)
        if stats.game_active :
            ship.update()
            gf.update_bullets(aliens, bullets, ai_settings, screen, ship, stats, sb)
            gf.update_alien(ai_settings, stats, screen, ship, aliens, bullets, sb)
            gf.update_screen(ai_settings, screen, ship, aliens, bullets, stats, play_button, sb)

run_game()