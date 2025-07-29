
# --- Specialized army generators for scenes ---

import random

from src.constants import SPRITE_VERTICAL_LOCATION
from src.generators.army_generator import generate_random_army


class BasicArmyGenerator:
    def __init__(self, color, num_soldiers, difficulty, interval, num_armies=1, base_location=0, location_range=None, set_location=None, delay=0):
        """basic army generator that spawns fixed number of soldiers at a fixed interval

        Args:
            color (string): color of the army
            num_soldiers (int): number of soldiers for each wave
            difficulty (string): difficulty of the army
            frequency (int): time between waves
            num_armies (int, optional): number of ammoes to generate. Defaults to 1.
            base_location (int, optional): location to spawn near. Defaults to 0.
        """
        self.color = color
        self.num_soldiers = num_soldiers
        self.difficulty = difficulty
        self.num_armies = num_armies

        # spawn locations
        self.base_location = base_location
        self.location_range = location_range
        self.set_location = set_location

        # time tracking
        self.spawned_count = 0
        self.last_spawn_time = delay
        self.interval = interval
        self.done = False

    def _generate_soldiers(self):
        """Generates a list of soldiers based on the parameters"""
        return generate_random_army(self.color, self.num_soldiers, self.difficulty, base_location=self.base_location, location_range=self.location_range, set_location=self.set_location)
    
    def __call__(self, dt):
        if self.done:
            return []

        if dt - self.last_spawn_time >= self.interval:
            self.last_spawn_time = dt
            self.spawned_count += 1

            if self.spawned_count >= self.num_armies:
                self.done = True

            return self._generate_soldiers()

        return []

class AbstractArmyGenerator():
    """Abstract class for army generators
    
    Allows for multiple basic army generators as well as offset time between them"""
    def __init__(self):
        self.generators = []
        self.done = False    # Whether the generators are fully completed

    def _begin_generator(self, dt): 
        if self.generators:
            for generator in self.generators:
                # subtract interval to allow generator to begin immediately
                # TODO: This can probably be done better
                # generator.last_spawn_time += dt - generator.interval
                generator.last_spawn_time = dt

    def __call__(self, dt):
        """Basic call function that loops through all generators and returns the combined result"""
        result = [soldier for generator in self.generators for soldier in generator(dt)]
        if all(generator.done for generator in self.generators):
            self.done = True

        return result

class CampArmyGenerator(AbstractArmyGenerator):
    def __init__(self):
        self.generators = [BasicArmyGenerator(color="blue", num_soldiers=3, difficulty="camp", interval=5, num_armies=5, base_location=2500), \
                            BasicArmyGenerator(color="red", num_soldiers=3, difficulty="camp", interval=8, num_armies=2, base_location=0, delay=8)]
        self.done = False

class ForestAmbushGenerator(AbstractArmyGenerator):
    def __init__(self):
        self.generators = [BasicArmyGenerator(color="blue", num_soldiers=3, difficulty="forest", interval=10, num_armies=6, base_location=2500), \
                            BasicArmyGenerator(color="blue", num_soldiers=4, difficulty="forest", interval=10, num_armies=6, base_location=2500, delay=5)]
        self.done = False

    def __call__(self, dt):
        # spawn soldiers in air as inactive and distribute them across the forest
        result1 = [*self.generators[0](dt)]
        for soldier in result1:
            soldier.active = False
            soldier.location = (random.randint(200, 1400), 200)

        # spawn soldiers at left and right of forest
        result2 = [*self.generators[1](dt)]
        for i, soldier in enumerate(result2):
            soldier.active = False
            soldier.location = (random.randint(*[-200, 0] if i > 1 else [1600, 1800]), SPRITE_VERTICAL_LOCATION)

        if self.generators[0].done and self.generators[1].done:
            self.done = True

        return [*result1, *result2]

class WallBattleSceneGeneratorBlue1(AbstractArmyGenerator):
    def __init__(self):
        # Adds blue mele reinforcements to the wall
        self.generators = [BasicArmyGenerator(color="blue", num_soldiers=4, difficulty="wall2", interval=8, num_armies=7, set_location=[-50, 2450], delay=2)]
        self.done = False

class WallBattleSceneGeneratorBlue2(AbstractArmyGenerator):
    def __init__(self):
        # Adds blue mele reinforcements to the wall
        self.generators = [BasicArmyGenerator(color="blue", num_soldiers=20, difficulty="wall3", interval=1, num_armies=1, base_location=2450)]
        self.done = False

class WallBattleSceneGeneratorRed(AbstractArmyGenerator):
    def __init__(self):
        # adds red units to climb ladders
        self.generators = [BasicArmyGenerator(color="red", num_soldiers=1, difficulty="red_army", interval=3, num_armies=15, set_location=[480, 1280, 2080])]
        self.done = False

    def __call__(self, dt):
        # spawn soldiers on ladders as inactive
        result = [*self.generators[0](dt)]
        for soldier in result:
            soldier.active = False
        
        if self.generators[0].done:
            self.done = True
        
        return result