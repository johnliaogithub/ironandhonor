import os

from src.constants import BACKGROUND_PATH, DEBUG, SPRITE_VERTICAL_LOCATION
from src.scenes.base import BattleScene, Restart, StoryScene, UIScene
from src.scenes.custom_scenes import (
    CampBattleScene,
    FieldBattleScene,
    ForestBattleScene,
    WallBattleScene,
)
from src.scenes.interactions import _guard_interaction
from src.units.base import BaseUnit
from src.units.player import Player
from src.units.soldier import Soldier

death_scene = UIScene(buttons=[
    {
        "text": "Restart",
        "position": (600, 400),
    }], text_elements=[
        {"text": "You have died!", "position": (100, 50)}
    ], next_scene=Restart())

# --- Scenes ---
def load_scenes() -> UIScene:
    BaseUnit.load_frames()

    guard = Soldier("red", False, "knight", location=(2000, SPRITE_VERTICAL_LOCATION), interaction=_guard_interaction)
    unarmored_player = Player("mc_unarmored", location=(240, SPRITE_VERTICAL_LOCATION))
    # armored_player = Player("mc_armored", location=(300, SPRITE_VERTICAL_LOCATION))

    # TODO: fix this
    to_be_continued = UIScene(text_elements=[
        {"text": "That's it for the demo! Please come back later for the continuation!",
        "position": (100, 50)}
    ])
    wall_scene = WallBattleScene()
    wall_scene.next_scene = to_be_continued
    field_scene = FieldBattleScene()
    field_scene.next_scene = wall_scene
    forestscene = ForestBattleScene()
    forestscene.next_scene = field_scene
    campscene2 = CampBattleScene()
    campscene2.next_scene = forestscene
    campscene = BattleScene(
        background_images=[os.path.join(BACKGROUND_PATH, "camp", "camp1.png"), os.path.join(BACKGROUND_PATH, "camp", "camp1.png"), os.path.join(BACKGROUND_PATH, "camp", "camp2.png")],
        next_scene=campscene2,
        units=[guard], 
        player=unarmored_player
    )
    introscene = StoryScene(["May 16th, 1401", "With the start of campaigning season, we have been rallied to invade the north.", 'We were told that they were "weak barbarians" and that we should "kill them all." ...'], [], next_scene=campscene)
    startscene = UIScene(buttons=[
        {
            "text": "Start Game",
            "position": (575, 400),
        }], title_element=
            {"title": "Welcome to Iron and Honor!", "position": (350, 150)}, next_scene=introscene)

    if DEBUG:
        startscene.next_scene = campscene2

    return startscene