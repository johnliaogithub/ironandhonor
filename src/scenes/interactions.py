from src.scenes.base import BattleScene
from src.units.interactives import InteractiveObject


# --- Interactions ---
def _guard_interaction(scene, player, unit):
    scene.on_interaction = True
    scene.instructions = {"name": "Guard", "text": ["Return to your tent, get your armor on and we will march on the", "enemy castle by noon!"]}

    # enable changing into armor
    scene.interactive_objects.append(InteractiveObject(240, _tent_interaction))

def _tent_interaction(scene, player, unit):
    scene.scene_complete = True

    # TODO: solve this issue, seems like shared interactive_objects, so I need to remove
    while scene.interactive_objects:
        scene.interactive_objects.pop()