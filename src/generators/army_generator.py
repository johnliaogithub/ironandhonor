import random

from src.constants import SPRITE_VERTICAL_LOCATION
from src.units.soldier import Soldier  # Adjust path as needed

unit_pool = {
    "camp":    ["spear"] * 5 + ["sword"] * 5 + ["knight"] * 1,
    "red_army":  ["spear"] * 1 + ["sword"] * 1 + ["knight"] * 1 + ["halberd"] * 1,
    "forest":  ["ambush_archer"] * 1 + ["ambush_sword"] * 1 + ["ambush_dagger"] * 1,    # Only for blue
    "field":     ["spear"] * 1 + ["sword"] * 1 + ["ambush_archer"] * 1 + ["peasant"] * 10,        # add peasant
    "wall":  ["spear"] * 1 + ["archer"] * 3 + ["sword"] * 1 + ["halberd"] * 1,
    "wall2":  ["spear"] * 2 + ["sword"] * 2 + ["halberd"] * 2 + ["knight"] * 1 + ["mace"] * 1,
    "wall3":    ["knight"] * 3 + ["mace"] * 3 + ["flail"] * 1 + ["axe"] * 1        # Only for blue
}

def generate_random_army(color, num_soldiers, difficulty, base_location=None, location_range:tuple[int, int]=None, set_location:list[int]=None):
    """
    Generate a list of Soldier objects based on army parameters.

    Args:
        color (str): "red" or "blue"
        num_soldiers (int): Number of units to generate
        difficulty (str): One of ["easy", "medium", "hard"]
        base_location (int): X coordinate to spawn near (e.g., 2500)

    Returns:
        List of Soldier objects
    """

    # Define unit types with weighted probabilities based on difficulty
    units = []

    for i in range(num_soldiers):
        unit_type = random.choice(unit_pool[difficulty])

        if location_range is not None:
            x_offset = random.randint(*location_range)
        elif set_location is not None:
            x_offset = set_location[random.randint(0, len(set_location) - 1)] + random.randint(-20, 20)
        else: 
            x_offset = base_location + random.randint(-100 - 10 * num_soldiers, 100 + 10 * num_soldiers)

        unit = Soldier(
            color=color,
            active=True,
            soldier_type=unit_type,
            location=(x_offset, SPRITE_VERTICAL_LOCATION)
        )
        units.append(unit)

    return units


# --- Specialized army generators for scenes ---
def forest_march_generator():
    soldiers = generate_random_army("red", 10, "red_army", -200)

    for i, soldier in enumerate(soldiers):
        soldier.location = (i * 200, soldier.location[1])
        soldier._animate("walk_right")
        soldier._animate("idle")  # TODO: fix this by making draw pause when interaction

    return soldiers