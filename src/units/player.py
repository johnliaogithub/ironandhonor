from src.units.base import BaseUnit
from src.constants import PLAYER_ATTACK_RANGE, SPRITE_VERTICAL_LOCATION

class Player(BaseUnit):
    """Main character class for the player unit."""

    def __init__(self, unit_type: str = 'mc_unarmored', location: tuple[int, int]=(0, SPRITE_VERTICAL_LOCATION)): 
        super().__init__(unit_type, "red")

        self.location = location

        self.animation_speed = 0.1
        self.timer = 0
        self.active = True

        self.attack_cooldown = 1
        self.attack_cooldown_timer = 0

        self.health = 200

    def act(self, action): 
        self._animate(action)

    def attack(self, units):
        if self.unit_type == "mc_unarmored":
            return

        # find all enemies in range and direction
        enemies_in_range = []
        facing_left = self.current_action.split("_")[-1] == "left"
        for unit in units:

            if unit.active and \
                unit.color != self.color and \
                abs(unit.location[0] - self.location[0]) <= PLAYER_ATTACK_RANGE and \
                (facing_left and unit.location[0] < self.location[0] or not facing_left and unit.location[0] > self.location[0]):

                enemies_in_range.append(unit)

        # if attacking (no matter if it's in range or not), complete attack animation
        if self.attacking:
            progress = self.animation_progress()

            # check if animation is at middle. deduct hp if enemy is still in range
            if progress[0] == 2:
                for enemy in enemies_in_range:
                    enemy.health -= self.attack_damage

            # check if animation is reached end. allow attack again if ended
            if progress[0] == progress[1] - 1: 
                self.attacking = False

                self.attack_cooldown_timer = self.attack_cooldown
                self.act("idle")

            return

        if self.attack_cooldown_timer > 0:
            self.attack_cooldown_timer -= 1
            return

        # attack
        self.attacking = True
        if facing_left: # if facing left
            self.act("hit_left")
        else: 
            self.act("hit_right")



    def draw(self, screen, camera):
        self._draw(screen, camera)