from src.constants import IDEAL_SPRITE_WIDTH, SPRITE_VERTICAL_LOCATION
from src.ui.text import draw_text_centered
from src.units.base import BaseUnit

# class Team(Enum): 
#     RED = 1
#     BLUE = 2

# class SoldierType(Enum):
#     SWORDSMAN = 1
#     SPEARMAN = 2
#     ARCHER = 3
#     KNIGHT = 4
#     MACE = 5
#     FLAIL = 6
#     HALBERD = 7
#     AXE = 8
#     DAGGER = 9

class Soldier (BaseUnit):

    def __init__(self, color: str = "red", active: bool = True, soldier_type = "knight", location: tuple[int, int]=(1000, SPRITE_VERTICAL_LOCATION), interaction=None):
        """
        Soldier class for the npcs in the game.
        interaction: function to call when interacting with the unit
            - can be dialogue, change scene, 
        """
        super().__init__(soldier_type, color)

        self.active = active  # Inactive for dead, static or story soldiers
    
        self.location = location

        self.interaction = interaction

        self.e_hover = False

        # Attacking mechanics, might need to move some of these to base
        self.attack_cooldown = 5
        self.attack_cooldown_timer = 0

        # Death mechanics
        self.dead = False
        self.dead_timer = 50        # How long before unit disappears
    
    def animate(self, action): 
        self._animate(action)

    def draw(self, screen, camera):
        self._draw(screen, camera)

        # For interact hover dialogue
        if self.e_hover: 
            text_position = (self.location[0], self.location[1] - 132)
            draw_text_centered(screen, "Press E to interact", camera.apply(text_position))

    def closest_enemy(self, units):
        closest_enemy = None
        for unit in units:
            if unit.active and unit.color != self.color:
                if closest_enemy is None or abs(unit.location[0] - self.location[0]) < abs(closest_enemy.location[0] - self.location[0]):
                    closest_enemy = unit

        return closest_enemy

    def attack_nearest_enemy(self, units, player):
        """Attack the nearest enemy if possible."""
        # find closest enemy
        closest_enemy = self.closest_enemy([*units, player])
        if closest_enemy is None: 
            self.animate("idle")
            return

        # if attacking (no matter if it's in range or not), complete attack animation
        if self.attacking:
            progress = self.animation_progress()

            # check if animation is at middle. deduct hp if enemy is still in range
            if progress[0] == 2:
                if abs(self.location[0] - closest_enemy.location[0]) <= IDEAL_SPRITE_WIDTH // 2:
                    closest_enemy.health -= self.attack_damage

            # check if animation is reached end. allow attack again if ended
            if progress[0] == progress[1] - 1: 
                self.attacking = False

                self.attack_cooldown_timer = self.attack_cooldown
                self.animate("idle")

            return

        if self.attack_cooldown_timer > 0:
            self.attack_cooldown_timer -= 1
            return

        # if not close enough to enemy, move towards closest enemy
        if self.location[0] - closest_enemy.location[0] > IDEAL_SPRITE_WIDTH // 2:
            self.location = (self.location[0] - 10, self.location[1])
            self.animate("walk_left")
        elif self.location[0] - closest_enemy.location[0] < -IDEAL_SPRITE_WIDTH // 2:
            self.location = (self.location[0] + 10, self.location[1])
            self.animate("walk_right")
        else: 
            # if close enough to enemy, attack
            self.attacking = True
            if self.location[0] < closest_enemy.location[0]:
                self.animate("hit_right")
            else: 
                self.animate("hit_left")

    def init_die(self):
        self.dead = True
        self.animate("dying")
    
    def loop_die(self)->bool:
        if self.current_action == "dying" and self.animation_progress()[0] == self.animation_progress()[1] - 1:
            self.animate("dead")

        if self.current_action == "dead":
            self.dead_timer -= 1

            if self.dead_timer <= 0:
                return True
        
        return False
    
    def interact(self, scene, target, unit):
        if self.interaction:
            self.interaction(scene, target, unit)