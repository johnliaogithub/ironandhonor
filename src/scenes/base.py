import pygame

from src.constants import IDEAL_SPRITE_WIDTH, SCREEN_HEIGHT
from src.scenes.camera import Camera
from src.ui.button import draw_button
from src.ui.text import draw_dialogue, draw_text
from src.units.player import Player


class BaseScene: 
    def draw(self, screen):
        """Draw the current scene."""
        pass

    def custom_pre_loop(self, actions, dt):
        pass

    def custom_post_loop(self, actions, dt):
        pass

class UIScene(BaseScene):
    """Base class for UI scenes, such as menu and start page."""

    def __init__(self, buttons=None, text_elements=None, background_image=None, next_scene=None):
        self.buttons = buttons if buttons else []
        self.text_elements = text_elements if text_elements else []
        self.background_image = background_image
        self.next_scene = next_scene
        self.button_rects = []

    def _loop(self, actions, dt):
        self.custom_pre_loop(actions, dt)

        for action in actions:
            # determine if button was clicked
            if action[0] == "click":
                pos = action[1]
                for button in self.button_rects:
                    if button.collidepoint(pos):
                        # placeholder, transition to next scene
                        return True
                    
        self.custom_post_loop(actions, dt)

        return False
    
    def draw(self, screen):
        """Draw the UI scene, including buttons and text elements."""
        if self.background_image:
            screen.blit(self.background_image, (0, 0))
        else:
            screen.fill((0, 0, 0))
        
        for button in self.buttons:
            self.button_rects.append(draw_button(screen, **button))

        for text in self.text_elements:
            draw_text(screen, **text)

class StoryScene(BaseScene):
    """Base class for story scenes, which may include dialogue and cutscenes.
    Follows the model of comic book storytelling.
    Continues to next panel or scene on enter."""

    def __init__(self, dialogue=None, cutscenes=None, background_image=None, next_scene=None):
        self.dialogue = dialogue if dialogue else []
        self.cutscenes = cutscenes if cutscenes else []
        self.background_image = background_image
        self.next_scene = next_scene
        self.progression = 0  # Current panel index in the dialogue or cutscene

    def _loop(self, actions, dt):
        """Process actions for the current scene.
        Returns True if the scene should transition to the next scene, False otherwise.
        """
        self.custom_pre_loop(actions, dt)

        for action in actions:
            if action == "enter":
                self.progression += 1
                if self.progression >= len(self.dialogue):
                    return True
        
        self.custom_post_loop(actions, dt)
                
        return False

    def draw(self, screen): 
        """Draw the current scene, including dialogue and cutscenes.
        Run every loop"""
        # default black background
        screen.fill((0, 0, 0))

        # Draw all cutscenes
        for i in range(self.progression):
            # Draw dialogue or cutscene panels
            # screen.blit(self.)
            pass

        # Draw last dialogue text
        draw_text(screen, self.dialogue[self.progression], (100, 50))



class BattleScene(BaseScene):
    """Base class for battle scenes, which may include combat mechanics and unit management."""
    def __init__(self, background_images=None, units=None, interactive_objects=None, next_scene=None, player=None, on_interaction=False, instructions=None, generator=None):
        self.background_images = background_images if background_images else []
        self.next_scene = next_scene

        # Placeholder for initiation logic
        self.player: Player = player if player else Player()
        self.units = units if units else []  # Placeholder for units involved in the battle
        self.interactive_objects = interactive_objects if interactive_objects else []
        self.camera = Camera(self.player, len(self.background_images) * SCREEN_HEIGHT)  # Assumes all background images are squares

        # For paused storyline events in the scene
        self.on_interaction = on_interaction if on_interaction else False
        self.instructions = instructions if instructions else {"name": None, "text": None}
        self.pan = False
        self.pan_location = (0, 0)

        self.scene_complete = False

        # for army generation
        self.generator = generator

    def _loop(self, mc_actions, dt):
        self.custom_pre_loop(mc_actions, dt)

        if self.player.health <= 0:
            from src.scenes.scene_list import death_scene
            self.next_scene = death_scene
            return True

        if self.on_interaction:
            for action in mc_actions:
                if action == "enter" or action == "space":
                    self.on_interaction = False
            return  # Don't process actions while interacting

        # Process actions for the current scene
        e_pressed = False
        
        if not self.player.attacking:
            for action in mc_actions:
                if action == "left":
                    self.player.location = (self.player.location[0] - 10, self.player.location[1])
                    self.player.act("walk_left")
                elif action == "right":
                    self.player.location = (self.player.location[0] + 10, self.player.location[1])
                    self.player.act("walk_right")
                elif action == "idle": 
                    self.player.act("idle")
                elif action == "space":
                    self.player.attack(self.units)
                elif action == "e":
                    e_pressed = True

        else: 
            self.player.attack(self.units) # TODO: kind of sketchy, try to fix

        # Process other interactions and decisions
        # Deal with interactive units
        for unit in self.units:
            if unit.active:
                unit.attack_nearest_enemy(self.units, self.player)

        for unit in self.units: # determine if unit is dead
            # kill if unit is dead
            if unit.active and unit.health <= 0:
                unit.active = False
                unit.init_die()

        for unit in self.units[:]:  # iterate over a copy
            if not unit.active:
                if unit.interaction: 
                    if unit.location[0] - IDEAL_SPRITE_WIDTH // 2 < self.player.location[0] < unit.location[0] + IDEAL_SPRITE_WIDTH // 2:
                        unit.e_hover = True
                        if e_pressed:
                            unit.interact(self, self.player, unit)
                    else:
                        unit.e_hover = False

                if unit.dead:
                    if unit.loop_die():
                        self.units.remove(unit)

        # Deal with interactive objects
        for _object in self.interactive_objects:
            # for some reason, self.interactive_objects is not empty

            if _object.x_position - IDEAL_SPRITE_WIDTH // 2 < self.player.location[0] < _object.x_position + IDEAL_SPRITE_WIDTH // 2:
                _object.e_hover = True

                if e_pressed:
                    _object.interact(self, self.player, unit)

            else: 
                _object.e_hover = False

        # Update camera
        self.camera.update()


        # Generate army if needed
        if self.generator:
            self.units.extend(self.generator(dt))
        
        self.custom_post_loop(mc_actions, dt)

        return self.scene_complete

    def draw_health_bar(self, screen, camera):
        """Draw a health bar on the screen."""
        border_radius = 10

        # Health bar dimensions
        x = 50
        y = 50
        width = 200
        height = 20

        # Colors
        background_color = (50, 50, 50)       # Dark gray
        border_color = (255, 255, 255)        # White
        health_color = (200, 0, 0)            # Red

        # Calculate health width
        health_ratio = max(0, min(self.player.health / 100, 1))  # Clamp between 0 and 1
        health_width = int(width * health_ratio)

        # Background (behind the health fill)
        pygame.draw.rect(screen, background_color, (x, y, width, height), border_radius=border_radius)
        pygame.draw.rect(screen, health_color, (x, y, health_width, height), border_radius=border_radius)
        pygame.draw.rect(screen, border_color, (x, y, width, height), width=2, border_radius=border_radius)

    def number_of_enemies(self):
        return len([unit for unit in self.units if unit.active and unit.color != self.player.color])

    def draw(self, screen):
        """Draw background images left to right, scaled to screen height."""
        if not hasattr(self, "_loaded_backgrounds"):
            self._loaded_backgrounds = []
            for path in self.background_images:
                image = pygame.image.load(path).convert()

                # Scale image to match screen height while preserving aspect ratio
                original_width, original_height = image.get_size()
                scale_factor = SCREEN_HEIGHT / original_height
                scaled_width = int(original_width * scale_factor)

                scaled_image = pygame.transform.scale(image, (scaled_width, SCREEN_HEIGHT))
                self._loaded_backgrounds.append(scaled_image)

        # Draw background images with camera offset
        x_offset = -self.camera.offset
        for image in self._loaded_backgrounds:
            screen.blit(image, (x_offset, 0))
            x_offset += image.get_width()

        # Draw units: 
        for unit in self.units:
            unit.draw(screen, self.camera)

        # Draw interactive objects
        for _object in self.interactive_objects:
            _object.draw(screen, self.camera)

        # Draw main character
        self.player.draw(screen, self.camera)
        if not self.on_interaction:
            self.draw_health_bar(screen, self.camera)

        # Update instructions
        if self.on_interaction:
            draw_dialogue(screen, self.instructions)