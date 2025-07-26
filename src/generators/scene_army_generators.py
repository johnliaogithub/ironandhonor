
# --- Specialized army generators for scenes ---

from src.generators.army_generator import generate_random_army


class BasicArmyGenerator:
    def __init__(self, color, num_soldiers, difficulty, interval, num_armies=1, base_location=0, time_offset=0):
        """basic army generator that spawns soldiers at a fixed interval

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
        self.base_location = base_location

        # time tracking
        self.spawned_count = 0
        self.last_spawn_time = time_offset
        self.interval = interval
        self.done = False

    def _generate_soldiers(self):
        """Generates a list of soldiers based on the parameters"""
        return generate_random_army(self.color, self.num_soldiers, self.difficulty, self.base_location)
    
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

class CampArmyGenerator():
    def __init__(self):
        self.blue_generator = BasicArmyGenerator(color="blue", num_soldiers=3, difficulty="camp", interval=5, num_armies=5, base_location=2500)
        self.red_generator = BasicArmyGenerator(color="red", num_soldiers=3, difficulty="camp", interval=8, num_armies=3, base_location=0, time_offset=5)
        self.done = False

    def __call__(self, dt):
        result = [*self.blue_generator(dt), *self.red_generator(dt)]
        if self.blue_generator.done and self.red_generator.done:
            self.done = True

        return result

class ForestAmbushGenerator():
    def __init__(self):
        self.blue_generator = BasicArmyGenerator(color="blue", num_soldiers=3, difficulty="camp", interval=5, num_armies=5, base_location=2500)
        self.done = False

    def __call__(self, dt):
        result = [*self.blue_generator(dt)]
        if self.blue_generator.done:
            self.done = True

        return result