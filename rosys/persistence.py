import logging
import json
import os
from .world import World


class Persistence:

    def __init__(self, world: World, filepath: str = '~/.rosys/world.json'):
        self.world = world
        self.filepath = os.path.expanduser(filepath)

    def dump(self) -> dict:
        return {
            'robot': {'parameters': self.world.robot.parameters.dict()},
            'cameras': {id: camera.dict() for id, camera in self.world.cameras.items()},
            'obstacles': {id: obstacle.dict() for id, obstacle in self.world.obstacles.items()},
        }

    def load(self, world: World):
        self.world.robot.parameters = world.robot.parameters
        self.world.cameras = world.cameras
        self.world.obstacles = world.obstacles

    def backup(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        with open(self.filepath, 'w') as f:
            json.dump(self.dump(), f)

    def parse_world(self, obj: dict):
        return World.parse_obj(obj)

    def restore(self):
        if not os.path.exists(self.filepath):
            logging.warning('No backup file found.')
            return
        try:
            with open(self.filepath, 'r') as f:
                self.load(self.parse_world(json.load(f)))
        except:
            logging.exception(f'Could not load from backup at {self.filepath}')
