import pygame
from src.ui.text import DEFAULT_TEXT_COLOR, DEFAULT_TEXT_FONT, draw_text


# def draw_button(screen, text, position, font=DEFAULT_TEXT_FONT, color=DEFAULT_TEXT_COLOR):
#     """Draw a button on the screen."""
#     # Draw button background
#     button_rect = pygame.Rect(position, (200, 50))
#     pygame.draw.rect(screen, (0, 0, 0), button_rect)
#     pygame.draw.rect(screen, (255, 255, 255), button_rect, 2)

#     # Draw button text
#     draw_text(screen, text, button_rect.topleft, font=font, color=color)

def draw_button(screen, text, position, font=DEFAULT_TEXT_FONT, text_color=DEFAULT_TEXT_COLOR,
                bg_color=(0, 0, 0), border_color=(255, 255, 255), padding=20):
    """
    position: (x, y) tuple for the top-left corner of the button
    Draw a centered button that sizes itself to the text."""
    # Render the text
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect()

    # Add padding to text size to determine button size
    button_width = text_rect.width + padding * 2
    button_height = text_rect.height + padding
    button_rect = pygame.Rect(0, 0, button_width, button_height)
    button_rect.center = position

    # Draw button background and border
    pygame.draw.rect(screen, bg_color, button_rect)
    pygame.draw.rect(screen, border_color, button_rect, 2)

    # Draw text centered inside the button
    text_rect.center = button_rect.center
    screen.blit(text_surf, text_rect)

    return button_rect  # Return the rect so you can check for clicks