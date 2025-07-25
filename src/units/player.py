from unittest.mock import seal
import pygame
from src.units.base import BaseUnit
from src.constants import SPRITE_VERTICAL_LOCATION

class Player(BaseUnit):
    """Main character class for the player unit."""

    def __init__(self, type='mc_unarmored', location=(0, SPRITE_VERTICAL_LOCATION)): 
        super().__init__(type, "red")

        self.location = location

        self.animation_speed = 0.1
        self.timer = 0
        self.active = True

    def act(self, action): 
        self._animate(action)


    def draw(self, screen, camera):
        self._draw(screen, camera)

        # Draw health bar
        # health_bar = pygame.Surface((100, 10))
        # pygame.draw.rect(health_bar, (0, 0, 0), (0, 0, health_bar.get_width() * self.health / 100, health_bar.get_height()))
        # screen.blit(health_bar, (self.location[0] - camera.offset - health_bar.get_width() / 2, self.location[1] - 128))