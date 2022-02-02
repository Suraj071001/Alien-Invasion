class Settings() :
    """A class to store all settings for Alien Invasion."""
    def __init__(self):
        # set screen,background color
        self.screen_width= 750
        self.screen_height=680
        self.bg_color=(129, 139, 231)

        #ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 5

        # alien settings
        self.fleet_drop_speed = 10
        #fleet_direction of 1 represent right , -1 represent left
        self.fleet_direction = 1

        #score
        self.alien_score = 50
        # How quickly the alien point values increase
        self.score_scale = 1.5

        # How quickly the game speeds up
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed_factor = 0.9
        self.bullet_speed_factor = 2
        self.alien_speed_factor = 0.2

    def increase_speed(self):
        """Increase speed settings."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_score = int(self.alien_score * self.score_scale)

