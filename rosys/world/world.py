from pydantic import BaseModel, PrivateAttr
from aenum import Enum, auto
import time

from .mode import Mode
from .obstacle import Obstacle
from .robot import Robot
from .camera import Camera
from .usb_camera import UsbCamera
from .upload import Upload


class AutomationState(str, Enum, init='value __doc__'):

    def _generate_next_value_(name, start, count, last_values):
        '''uses enum name as value when calling auto()'''
        return name

    DISABLED = auto(), 'no automations available or execution not allowed'
    STOPPED = auto(), 'there is an automation which could be started'
    RUNNING = auto(), 'automations are beeing processed'
    PAUSED = auto(), 'an ongoing automation can be resumed'


class World(BaseModel):
    robot: Robot = Robot()
    mode: Mode = Mode.REAL
    automation_state: AutomationState = AutomationState.DISABLED
    _time: float = PrivateAttr(default_factory=time.time)
    obstacles: dict[str, Obstacle] = {}
    notifications: list[tuple[float, str]] = []
    cameras: dict[str, Camera] = {}
    upload: Upload = Upload()

    @property
    def time(self):
        return self._time if self.mode == Mode.TEST else time.time()

    def set_time(self, value):
        assert self.mode == Mode.TEST
        self._time = value

    @property
    def usb_cameras(self) -> dict[str, UsbCamera]:
        return {c.id: c for c in self.cameras.values() if isinstance(c, UsbCamera)}
