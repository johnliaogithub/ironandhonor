# UI Text Elements

import os
import pygame

from src.constants import SCREEN_HEIGHT, SCREEN_WIDTH

pygame.font.init()

DEFAULT_TEXT_FONT = pygame.font.Font(os.path.join("assets", "fonts", "PixelifySans-VariableFont_wght.ttf"), 24)
DEFAULT_TEXT_COLOR = (255, 255, 255)
RED = (202, 52, 52)

DEFAULT_TITLE_FONT = pygame.font.Font(os.path.join("assets", "fonts", "PixelifySans-VariableFont_wght.ttf"), 36)

def draw_text(screen, text, position, font=DEFAULT_TEXT_FONT, color=DEFAULT_TEXT_COLOR):
    """Draw text on the screen at a specified position."""
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

def draw_text_centered(screen, text, position, font=DEFAULT_TEXT_FONT, color=DEFAULT_TEXT_COLOR):
    """Draw text on the screen at a specified position, centered."""
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (position[0] - text_surface.get_width() // 2, position[1] - text_surface.get_height() // 2))

def create_box(size, position, screen):
    """Create and draw a semi-transparent rounded box on the screen."""
    # Create a surface with per-pixel alpha
    box_surface = pygame.Surface(size, pygame.SRCALPHA)
    
    # Draw a semi-transparent rounded rectangle onto the box surface
    rect = pygame.Rect(0, 0, *size)
    pygame.draw.rect(box_surface, (0, 0, 0, 150), rect, border_radius=10)
    
    # Now blit the fully drawn box surface to the screen
    screen.blit(box_surface, position)

    return box_surface

def draw_text_in_box(screen, text, position, font=DEFAULT_TEXT_FONT, color=DEFAULT_TEXT_COLOR):
    """Draw text on the screen at a specified position with a background box."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(topleft=position)

    # Draw a semi-transparent background box
    create_box(text_rect.size, text_rect.topleft, screen)

    screen.blit(text_surface, text_rect.topleft)

def draw_dialogue(screen, instructions):
    """Draw dialogue on the screen."""
    create_box((SCREEN_WIDTH - 180, 100), (90, 40), screen)

    # Draw red text for instructions.name and black text for instructions.text
    draw_text(screen, f"{instructions['name']}:", (100, 50), color=RED)

    # Definitely going to need to change this
    for i, text in enumerate(instructions["text"]):
        draw_text(screen, text, (200, 50 + i * 25))