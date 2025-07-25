from src.constants import INTERACTIVE_TEXT_Y
from src.ui.text import draw_text_centered


class InteractiveObject:
    def __init__(self, x_position, interaction):
        self.x_position = x_position

        self.interaction = interaction
        self.e_hover = False

    def draw(self, screen, camera):
        if self.e_hover: 
            text_position = (self.x_position, INTERACTIVE_TEXT_Y)
            draw_text_centered(screen, "Press E to interact", camera.apply(text_position))
    
    def interact(self, scene, target, unit):
        self.interaction(scene, target, unit)