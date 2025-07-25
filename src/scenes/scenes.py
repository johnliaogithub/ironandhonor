import os
from src.constants import SPRITE_VERTICAL_LOCATION, BACKGROUND_PATH
from src.scenes.base import BattleScene, StoryScene, UIScene
from src.scenes.interactions import _guard_interaction
from src.units.base import BaseUnit
from src.units.soldier import Soldier
from src.units.player import Player

death_scene = UIScene(buttons=[
    {
        "text": "Restart",
        "position": (600, 400),
    }], text_elements=[
        {"text": "You have died!", "position": (100, 50)}
    ], next_scene=None)

# --- Scenes ---
def load_scenes():
    BaseUnit.load_frames()

    guard = Soldier("red", False, "knight", location=(2000, SPRITE_VERTICAL_LOCATION), interaction=_guard_interaction)
    unarmored_player = Player("mc_unarmored", location=(240, SPRITE_VERTICAL_LOCATION))
    armored_player = Player("mc_armored", location=(300, SPRITE_VERTICAL_LOCATION))

    campscene2 = BattleScene(
        background_images=[os.path.join(BACKGROUND_PATH, "camp", "camp1.png"), os.path.join(BACKGROUND_PATH, "camp", "camp1.png"), os.path.join(BACKGROUND_PATH, "camp", "camp2.png")],
        next_scene=None,
        #units=[Soldier("blue", True, "sword", location=(2400, SPRITE_VERTICAL_LOCATION)), Soldier("blue", True, "knight", location=(2500, SPRITE_VERTICAL_LOCATION))], 
        units=[Soldier("blue", True, "knight", location=(2500, SPRITE_VERTICAL_LOCATION))], 
        player=armored_player, 
        on_interaction=True,
        instructions={"name": "Guard", "text": ["To arms! The enemies are attacking our camp!"]}
    )
    # campscene = BattleScene(
    #     background_images=[os.path.join(BACKGROUND_PATH, "camp", "camp1.png"), os.path.join(BACKGROUND_PATH, "camp", "camp1.png"), os.path.join(BACKGROUND_PATH, "camp", "camp2.png")],
    #     next_scene=campscene2,
    #     units=[guard], 
    #     player=unarmored_player
    # )
    # introscene = StoryScene(["And so it begins..."], [], next_scene=campscene)
    # introscene = StoryScene(["And so it begins..."], [], next_scene=campscene)
    startscene = UIScene(buttons=[
        {
            "text": "Start Game",
            "position": (600, 400),
        }], text_elements=[
            {"text": "Welcome to Iron and Honor!", "position": (100, 50)}
        # ], next_scene=introscene)
        ], next_scene=campscene2)
    return startscene