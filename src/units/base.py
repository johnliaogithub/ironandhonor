import json
import os

import pygame

from src.constants import ROW_HEIGHT, IDEAL_SPRITE_HEIGHT, SPRITE_VERTICAL_LOCATION, IDEAL_SPRITE_WIDTH, UNIT_PATH

class BaseUnit: 
    _default_sheet_locations = {
        "idle": {
            "num_frames": 1,
            "frame_width": 64,
            "frame_height": 64,
            "row": 2
        },
        "walk_left": {
            "num_frames": 8,
            "frame_width": 64,
            "frame_height": 64,
            "row": 9
        },
        "walk_right": {
            "num_frames": 8,
            "frame_width": 64,
            "frame_height": 64,
            "row": 11
        },
        "idle_left": {
            "num_frames": 1,
            "frame_width": 64,
            "frame_height": 64,
            "row": 9
        },
        "idle_right": {
            "num_frames": 1,
            "frame_width": 64,
            "frame_height": 64,
            "row": 11
        },
        "dying": {
            "num_frames": 6,
            "frame_width": 64,
            "frame_height": 64,
            "row": 20
        },
        "dead": {
            "num_frames": 1,
            "frame_width": 64,
            "frame_height": 64,
            "row": 20,
            "skip": 5
        }
    }

    
    _unit_data = {}

    _frames = {}  # Dictionary of frames for each action for each soldier type and color

    _unique_blue_units = ["ambush_archer", "ambush_sword", "ambush_dagger", "flail", "axe"]

    def __init__(self, unit_type, color):
        self.unit_type = unit_type
        self.color = color
        self.position = 0
        
        self.location = (0, SPRITE_VERTICAL_LOCATION)
        self.frame_index = 0
        
        self.current_sprite_dimensions = (64, 64)

        self.current_action = ""
        self._animate("idle")

        self.health = 100
        self.attacking = False
        self.attack_damage = self._unit_data[self.unit_type]["attack_damage"]

    def get_center_x(self):
        """Going to need to deal with color"""
        return self.location[0]
    
    @classmethod
    def load_frames(cls):
        """issues: each sprite sheet loaded the number of times as actions"""
        # Load json file
        with open(os.path.join("src", "units", "soldiers.json")) as f:
            cls._unit_data = json.load(f)

        # Extract and load frames for each soldier type
        # Note: mc_unarmored and mc_armored will be considered different soldier types
        cls._frames = {}
        for unit_type, data in cls._unit_data.items():
            # Add default sheet locations to unit data
            cls._unit_data[unit_type]["actions"] = {**cls._default_sheet_locations, **data["actions"]}
    
            cls._frames[unit_type] = {"red": {}, "blue": {}}

            blue_sheet = pygame.image.load(os.path.join(UNIT_PATH, unit_type, "blue_" + unit_type + ".png")).convert_alpha() if unit_type != "mc_unarmored" and unit_type != "mc_armored" else None
            red_sheet = pygame.image.load(os.path.join(UNIT_PATH, unit_type, "red_" + unit_type + ".png")).convert_alpha() if unit_type not in cls._unique_blue_units else None
            for action, action_data in cls._unit_data[unit_type]["actions"].items():
                if unit_type == "mc_unarmored" or unit_type == "mc_armored":
                    cls._frames[unit_type]["red"][action] = cls.extract_frames_for_action(red_sheet, **action_data)
                    continue

                # load blue
                cls._frames[unit_type]["blue"][action] = cls.extract_frames_for_action(blue_sheet, **action_data)

                # load red
                if unit_type in cls._unique_blue_units:
                    continue
                cls._frames[unit_type]["red"][action] = cls.extract_frames_for_action(red_sheet, **action_data)
                
    
    @classmethod
    def extract_frames_for_action(cls, sprite_sheet, row:int, frame_width:int, frame_height:int, num_frames:int, skip:int=0):
        """Extract frames for a specific action from a sprite sheet.
        Note: scaling is done in transform.scale, might need to make the code cleaner"""
        frames = []
        for i in range(num_frames):
            frame = cls.extract_frame(sprite_sheet, i * frame_width + skip * frame_width, row * ROW_HEIGHT, frame_width, frame_height)
            frame = pygame.transform.scale(frame, (frame_width * IDEAL_SPRITE_WIDTH / 64, frame_height * IDEAL_SPRITE_HEIGHT / 64))
            frames.append(frame)

        return frames
    
    @classmethod
    def extract_frame(cls, sheet, x, y, width, height):
        """Extract a single frame from a sprite sheet."""
        frame = pygame.Surface((width, height), pygame.SRCALPHA)
        frame.blit(sheet, (0, 0), (x, y, width, height))
        return frame
    
    @classmethod
    def get_frames(cls, unit_type, color, action):
        return cls._frames[unit_type][color][action]

    def get_unit_data(self):
        return self._unit_data[self.unit_type]["actions"]

    def get_current_action_data(self):
        return self.get_unit_data()[self.current_action]

    def _animate(self, action):
        """Change the units animation state based on the action."""
        if self.current_action == action: 
            return 

        if action == "idle":
            if self.current_action in ["walk_left", "run_left", "hit_left", "idle_left"]:
                self.current_action = "idle_left"
            elif self.current_action in ["walk_right", "run_right", "hit_right", "idle_right"]:
                self.current_action = "idle_right"
            else: 
                self.current_action = "idle"
        else: 
            self.current_action = action

        self.frame_index = 0

        # Update sprite dimensions
        self.current_sprite_dimensions = self.get_current_action_data()["frame_width"] * IDEAL_SPRITE_WIDTH / 64, self.get_current_action_data()["frame_height"] * IDEAL_SPRITE_HEIGHT / 64

    def animation_progress(self): 
        return self.frame_index, len(self.get_frames(self.unit_type, self.color, self.current_action))
    
    def _draw(self, screen, camera):
        current_frames = self.get_frames(self.unit_type, self.color, self.current_action)

        # why does this work? I have no fucking idea: 
        top_left = (self.location[0] - camera.offset - self.current_sprite_dimensions[0] / 2, self.location[1] - 128)
        screen.blit(current_frames[self.frame_index], top_left)

        # Update frame index
        self.frame_index = (self.frame_index + 1) % len(current_frames)