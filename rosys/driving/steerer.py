import logging
from enum import Enum

import rosys
from rosys.event import Event

from .drivable import Drivable


class State(Enum):
    IDLE = 1
    STEERING = 2
    STOPPING = 3


class Steerer:
    STEERING_STARTED = Event()
    '''steering has started'''

    STEERING_STOPPED = Event()
    '''steering has stopped'''

    speed_scaling: float = 1

    def __init__(self, wheels: Drivable) -> None:
        self.log = logging.getLogger('rosys.steerer')

        self.wheels = wheels
        self.state = State.IDLE
        self.linear_speed = 0
        self.angular_speed = 0

        rosys.on_repeat(self.step, 0.05)

    def start(self) -> None:
        self.log.info('start steering')
        self.state = State.STEERING
        self.STEERING_STARTED.emit()

    def update(self, x: float, y: float) -> None:
        if self.state == State.STEERING:
            self.linear_speed = y * self.speed_scaling
            self.angular_speed = -x * self.speed_scaling

    def stop(self) -> None:
        self.log.info('stop steering')
        self.orientation = None
        self.state = State.STOPPING
        self.STEERING_STOPPED.emit()

    async def step(self) -> None:
        if self.state == State.STEERING:
            await self.wheels.drive(self.linear_speed, self.angular_speed)
        elif self.state == State.STOPPING:
            await self.wheels.stop()
            self.state = State.IDLE

    def __str__(self) -> str:
        return f'{type(self).__name__} ({self.state})'