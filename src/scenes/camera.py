import pygame
from src.constants import SCREEN_HEIGHT, SCREEN_WIDTH

class Camera:
    def __init__(self, main_character, battle_field_width):
        """Initialize the camera with the main character. Only horizontal scrolling is supported."""

        self.offset = 0

        self.camera_status = "Follow"  # None, Hold, Follow, Pan
        self.mc = main_character

        self.battle_field_width = battle_field_width

        self.target_offset: pygame.Vector2 = None
        self.pan_speed = 10

    def update(self):
        if self.camera_status == "Follow":
            # Center the camera on the target
            self.offset = min(max(self.mc.get_center_x() - SCREEN_WIDTH // 2, 0), self.battle_field_width - SCREEN_WIDTH)
        elif self.camera_status == "Pan":
            if self.target_offset - self.offset > self.pan_speed:
                self.offset += self.pan_speed
            elif self.target_offset - self.offset < -self.pan_speed:
                self.offset -= self.pan_speed
            else:
                self.offset = self.target_offset

    def change_status(self, status):
        self.camera_status = status

    def apply(self, position: tuple=(0, 0)):
        """Return a new rect shifted by the camera offset."""
        """isn't used for now"""
        return (position[0] - self.offset, position[1])
