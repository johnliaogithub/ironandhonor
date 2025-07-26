import random

from src.constants import SPRITE_VERTICAL_LOCATION
from src.units.soldier import Soldier  # Adjust path as needed

unit_pool = {
    "camp":    ["spear"] * 5 + ["sword"] * 5 + ["knight"] * 1,
    "forest":  ["ambush_archer"] * 1 + ["ambush_sword"] * 1 + ["ambush_dagger"] * 1,    # Only for blue
    "field":     ["spear"] * 1 + ["sword"] * 1 + ["archer"] * 1,        # add peasant
    "wall":  ["spear"] * 2 + ["archer"] * 2 + ["sword"] * 1 + ["knight"] * 1,
    "hard":    ["spear"] * 2 + ["sword"] * 2 + ["knight"] * 1 + ["mace"] * 1,
    "very_hard":    ["knight"] * 3 + ["mace"] * 3 + ["flail"] * 1 + ["axe"] * 1        # Only for blue
}

def generate_random_army(color, num_soldiers, difficulty, base_location):
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
    spacing_range = 80  # Random spacing between units

    for i in range(num_soldiers):
        unit_type = random.choice(unit_pool[difficulty])
        x_offset = base_location + i * spacing_range + random.randint(-15, 15)
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
    soldiers = generate_random_army("red", 10, "camp", -200)

    for i, soldier in enumerate(soldiers):
        soldier.location = (i * 200, soldier.location[1])
        soldier._animate("walk_right")
        soldier._animate("idle")  # TODO: fix this by making draw pause when interaction

    return soldiers