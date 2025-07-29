# --- Custom scenes (if required) ---
import itertools
import os

from src.constants import BACKGROUND_PATH, SPRITE_VERTICAL_LOCATION
from src.generators.army_generator import forest_march_generator, generate_random_army
from src.generators.scene_army_generators import (
    CampArmyGenerator,
    ForestAmbushGenerator,
    WallBattleSceneGeneratorBlue1,
    WallBattleSceneGeneratorBlue2,
    WallBattleSceneGeneratorRed,
)
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
        
        # End of the scene
        self.delay = 2
        self.finish_time = None
        self.new_instructions = {"name": "Commander", "text": ["Many of our soldiers have been killed, but we cannot stop now..."]}
        self.ready_for_next_scene = False

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
        
        else: 
            if "enter" in actions:
                # begin ambush
                self.generator._begin_generator(dt)

            # ambush
            for soldier in self.units:
                if not soldier.active and not soldier.dead:
                    # make soldier fall

                    # fall speed is inversely proportional to distance from enemy
                    fall_speed = 10 + soldier.location[1] / 20
                    soldier.location = (soldier.location[0], soldier.location[1] + fall_speed)

                    if soldier.location[1] >= SPRITE_VERTICAL_LOCATION:
                        soldier.active = True
                        soldier.location = (soldier.location[0], SPRITE_VERTICAL_LOCATION)

            # Scene completion
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

class FieldBattleScene(BattleScene):
    def __init__(self):
        super().__init__(
            background_images=[os.path.join(BACKGROUND_PATH, "castlefront", "castlefront{}.png".format(i + 1)) for i in range(3)],
            next_scene=None,
            units=[*generate_random_army("red", 4, "red_army", -500), *generate_random_army("blue", 15, "field", location_range=(500, 2500))],
            player=Player("mc_armored", location=(0, SPRITE_VERTICAL_LOCATION)),
            on_interaction=True,
            instructions={"name": "Commander", "text": ["Kill their peasants!"]}
        )

        self.delay = 2
        self.finish_time = None
        self.new_instructions = {"name": "Commander", "text": ["Good work. Our fallen soldiers are avenged!"]}
        self.ready_for_next_scene = False

    def custom_post_loop(self, actions, dt):
        if self.number_of_enemies() == 0:
            # fight complete
            if self.finish_time is None:
                self.finish_time = dt
            elif self.ready_for_next_scene:
                self.scene_complete = True
            elif dt - self.finish_time >= self.delay:
                self.on_interaction = True
                self.instructions = self.new_instructions
                self.ready_for_next_scene = True

class WallBattleScene(BattleScene): 
    def __init__(self):
        super().__init__(
            background_images=[os.path.join(BACKGROUND_PATH, "wall", "wall2.png"), os.path.join(BACKGROUND_PATH, "wall", "wall1.png"), os.path.join(BACKGROUND_PATH, "wall", "wall1.png")],
            next_scene=None,
            units=[*generate_random_army("blue", 12, "wall", location_range = (-200, 2700)),                             # generates blue archers, spearmen, halberds and swordsmen along the wall
                *generate_random_army("red", 3, "red_army", 480), *generate_random_army("red", 3, "red_army", 1280), *generate_random_army("red", 3, "red_army", 2080)],                   # TODO: generates red soldiers on ladder positions
            player=Player("mc_armored", location=(500, SPRITE_VERTICAL_LOCATION)),
            on_interaction=True,
            instructions={"name": "Commander", "text": ["Create an opening for our forces!"]},
            generator=WallBattleSceneGeneratorBlue1()
        )

        # backgrounds: 
        self.secondary_background = self.load_backgrounds([os.path.join(BACKGROUND_PATH, "wall", "wall_secondary.png")] * 2)
        self.climbing_units = []    # all units that are climbing up the wall

        self.current_phase = 1

        # First phase: fighting on the wall, red and blue generators
        self.red_generator = WallBattleSceneGeneratorRed()

        # Second phase: reinforcements arrive
        self.blue_generator = WallBattleSceneGeneratorBlue2()
        self.delay = 4
        self.finish_time = None
        self.new_instructions = {"name": "Commander", "text": ["Enemy reinforcements have arrived!"]}
        self.ready_for_next_part = False

        # Third phase: run away towards left side, no need to press e
        self.new_instructions2 = {"name": "", "text": ["I think I should run ..."]}
        

    def custom_pre_loop(self, actions, dt):
        if self.red_generator:
            self.climbing_units.extend(self.red_generator(dt)) # TODO: fix this

    def custom_post_loop(self, actions, dt):
        if self.current_phase == 1: 
            if self.red_generator.done and self.generator.done and self.number_of_enemies() == 0:
                # move to second phase
                self.current_phase = 2
                self.on_interaction = True
                self.red_generator = None
                self.instructions = self.new_instructions
                self.generator = self.blue_generator
                return
            
            if "enter" in actions:
                self.red_generator._begin_generator(dt)
            
            for soldier in self.climbing_units[:]:
                if soldier.location[1] < 400: 
                    # TODO: change constant
                    self.units.append(soldier)
                    self.climbing_units.remove(soldier)
                else: 
                    soldier.location = (soldier.location[0], soldier.location[1] - 10)

            for soldier in filter(lambda soldier: not soldier.active and not soldier.dead, self.units):
                if soldier.location[1] > SPRITE_VERTICAL_LOCATION:
                    soldier.location = (soldier.location[0], SPRITE_VERTICAL_LOCATION)
                    soldier.active = True
                else:
                    soldier.location = (soldier.location[0], soldier.location[1] + 10)
            
        elif self.current_phase == 2:
            
            if "enter" in actions:
                self.blue_generator._begin_generator(dt)

            if self.finish_time is None:
                self.finish_time = dt
            elif self.ready_for_next_part:
                self.current_phase = 3
            elif dt - self.finish_time >= self.delay:
                self.on_interaction = True
                self.instructions = self.new_instructions2
                self.ready_for_next_part = True

        elif self.current_phase == 3:
            if self.player.location[0] < 50:
                # ran away
                self.scene_complete = True

    def custom_pre_draw(self, screen):
        # display secondary background, with slightly slower camera offset
        x_offset = -self.camera.offset / 3
        for image in self.secondary_background:
            screen.blit(image, (x_offset, 0))
            x_offset += image.get_width()

        # display soldiers behind primary background
        for unit in self.climbing_units:
            unit.draw(screen, self.camera)