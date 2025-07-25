import pygame
from src.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from src.scenes.scenes import load_scenes

class Game: 

    def __init__(self):
        # Initialize game state
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Iron and Honor")

        self.clock = pygame.time.Clock()
        
        self.current_scene = load_scenes()

    def run(self): 
        """Start the game loop."""
        clock = pygame.time.Clock()

        while True: 
            # --- Recieve actions ---
            actions = []
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return 
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    actions.append(("click", pos))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]: 
                actions.append("enter")
            elif keys[pygame.K_LEFT]:
                actions.append("left")
            elif keys[pygame.K_RIGHT]:
                actions.append("right")
            elif keys[pygame.K_SPACE]:
                actions.append("space")
            else: 
                actions.append("idle")

            # Handle interaction
            if keys[pygame.K_e]: 
                actions.append("e")

            # --- Process actions ---
            if self.current_scene.action(actions): 
                self.current_scene = self.current_scene.next_scene
                continue # continue to next scene

            # --- Update draw ---
            if self.current_scene:
                self.current_scene.draw(self.screen)

            # --- Update game state ---
            pygame.display.flip()

            clock.tick(20)