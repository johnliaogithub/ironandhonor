# --- Custom scenes (if required) ---
import os

from src.constants import BACKGROUND_PATH, SPRITE_VERTICAL_LOCATION
from src.generators.army_generator import forest_march_generator, generate_random_army
from src.generators.scene_army_generators import CampArmyGenerator
from src.scenes.base import BattleScene
from src.units.player import Player
from src.units.soldier import Soldier


class CampBattleScene(BattleScene):
    def __init__(self):
        super().__init__(
            background_images=[os.path.join(BACKGROUND_PATH, "camp", "camp1.png"), os.path.join(BACKGROUND_PATH, "camp", "camp1.png"), os.path.join(BACKGROUND_PATH, "camp", "camp2.png")],
            next_scene=None,
            units=[*generate_random_army("red", 4, "camp", -500), *generate_random_army("blue", 7, "camp", 2500)],
            player=Player("mc_armored", location=(300, SPRITE_VERTICAL_LOCATION)),
            on_interaction=True,
            instructions={"name": "Guard", "text": ["To arms! The enemies are attacking our camp!"]},
            generator=CampArmyGenerator()
        )

        self.delay = 2
        self.finish_time = None
        self.new_instructions = {"name": "Guard", "text": ["The enemies are defeated! We will march on their castle!"]}
        self.ready_for_next_scene = False
    
    def custom_post_loop(self, actions, dt):
        if self.generator.done and self.number_of_enemies() == 0:
            # fight complete
            if self.finish_time is None:
                self.finish_time = dt
            elif self.ready_for_next_scene:
                self.scene_complete = True
            elif dt - self.finish_time >= self.delay:
                self.on_interaction = True
                self.instructions = self.new_instructions
                self.ready_for_next_scene = True


class DummySoldier(Soldier):
    """Soldier that does nothing. Used to cause red soldiers to march."""
    def __init__(self):
        super().__init__("blue", True, "spear", (3000, SPRITE_VERTICAL_LOCATION))

    def attack_nearest_enemy(self, units, player):
        pass

class ForestBattleScene(BattleScene):
    def __init__(self):
        self.dummy_soldier = DummySoldier()

        super().__init__(
            background_images=[os.path.join(BACKGROUND_PATH, "forest", "forest.png") for _ in range(2)],
            next_scene=None,
            units=[*forest_march_generator(), self.dummy_soldier],
            player=Player("mc_armored", location=(100, SPRITE_VERTICAL_LOCATION)),
            on_interaction=True,
            instructions={"name": "Commander", "text": ["Follow the marching column to the enemy castle."]}
        )

        # First part of the scene
        self.marching = True

    def custom_post_loop(self, actions, dt):
        if self.marching: 
            # If soldier reaches end, move it to beginning
            for soldier in self.units:
                # skip dummy soldier
                if soldier.__class__.__name__ == "DummySoldier":
                    continue
                if soldier.location[0] > 2000:
                    soldier.location = (0, soldier.location[1])

            if self.player.location[0] > 1400: # Threshold at which marching ends and ambush begins
                self.marching = False
                self.on_interaction = True
                self.instructions = {"name": "Commander", "text": ["Ambush!"]}

                # remove placeholder enemy soldier
                self.units.remove(self.dummy_soldier)

                # begin ambush
                self.generator = ForestAmbushGenerator()
        
        
        
        