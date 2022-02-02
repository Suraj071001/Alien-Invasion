import sys
from time import sleep

import pygame
from bullet import Bullet
from alien import Alien



def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (ai_settings.screen_height -(3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number,row_number):
    """Create an alien and place it in the row."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    alien.rect.x = alien.x
    aliens.add(alien)

def create_fleet(ai_settings, screen, aliens, ship):
    """Create a full fleet of aliens."""
    # Create an alien and find the number of aliens in a row.
    # Spacing between each alien is equal to one alien width.
    alien=Alien(ai_settings,screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,alien.rect.height)

    # Create the first row of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,row_number)

def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet if limit not reached yet."""
    if len(bullets) < ai_settings.bullets_allowed:
        # Create a new bullet and add it to the bullets group.
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def event_keydown_check(event,ai_settings,screen,ship,bullets) :
    if event.key == pygame.K_RIGHT:
        # move the ship to the right
        ship.moving_right = True

    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)

    elif event.key == pygame.K_q:
        sys.exit()

    elif event.key == pygame.K_LEFT:
        # move ship to the left
        ship.moving_left = True

def event_keyup_check(event,ship) :
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False

    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def event_check(ai_settings, screen,ship,bullets,stats,play_button,aliens,sb) :
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN :
            event_keydown_check(event,ai_settings,screen,ship,bullets)

        elif event.type == pygame.KEYUP :
            event_keyup_check(event,ship)

        elif event.type == pygame.MOUSEBUTTONDOWN :
            mouse_x , mouse_y = pygame.mouse.get_pos()
            check_play_button(stats,play_button,mouse_x,mouse_y,ai_settings,screen,aliens,ship,bullets,sb)

def update_screen(ai_settings,screen,ship,aliens,bullets,stats,play_button,sb) :
    screen.fill(ai_settings.bg_color)
    sb.show_score()
    # Redraw all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullets()
    ship.blitme()
    aliens.draw(screen)
    # Draw the play button if the game is inactive.
    if not stats.game_active:
        play_button.draw_button()
    # Make the most recently drawn screen visible.
    pygame.display.flip()

def update_bullets(aliens,bullets,ai_settings,screen,ship,stats,sb) :
    """Update position of bullets and get rid of old bullets."""
    # Update bullet positions.
    bullets.update()
    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets,stats,sb)

def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets,stats,sb):
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions :
        for a in collisions.values() :
            stats.score += ai_settings.alien_score * len(a)
            sb.prep_score()
        check_high_score(stats, sb)

    #for create new fleet of aliens and no bullets fire at that moment
    if len(aliens) == 0 :
        bullets.empty()
        ai_settings.increase_speed()
        stats.game_level += 1
        sb.prep_level()
        create_fleet(ai_settings,screen,aliens,ship)
    # Get rid of bullets that have disappeared.

def change_fleet_direction(ai_settings,aliens):
    """drop the entire fleet and change the direction"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *=-1

def check_fleet_edges(ai_settings,aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break

def update_alien(ai_settings, stats, screen, ship, aliens, bullets,sb) :
    """check if the fleet is in edge and then
    update the position of all aliens in the fleet"""
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship,aliens) :
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets,sb)
    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets,sb)

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets,sb):
    """Respond to ship being hit by alien."""
    # Decrement ships_left.
    if stats.ships_left > 0 :
        stats.ships_left -= 1

        #update a scoreboard
        sb.prep_ship()

        # pause
        sleep(1)

        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        ship.center_ship()
        create_fleet(ai_settings, screen, aliens, ship)

    else :
        pygame.mouse.set_visible(True)
        stats.game_active = False

def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets,sb):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites() :
        if alien.rect.bottom > screen_rect.bottom :
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets,sb)

def check_play_button(stats,play_button,mouse_x,mouse_y,ai_settings,screen,aliens,ship,bullets,sb) :
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active :
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        ai_settings.initialize_dynamic_settings()
        stats.game_active = True
        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()

        # Reset the scoreboard images.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ship()

        # Create a new fleet and center the ship.
        ship.center_ship()
        create_fleet(ai_settings, screen, aliens, ship)

def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()