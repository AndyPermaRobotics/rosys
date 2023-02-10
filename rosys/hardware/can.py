from .module import ModuleHardware
from .robot_brain import RobotBrain


class CanHardware(ModuleHardware):

    def __init__(self, robot_brain: RobotBrain, *,
                 name: str = 'can',
                 rx_pin: int = 32,
                 tx_pin: int = 33,
                 baud: int = 1_000_000) -> None:
        self.name = name
        lizard_code = f'{name} = Can({rx_pin}, {tx_pin}, {baud})'
        super.__init__(robot_brain=robot_brain, lizard_code=lizard_code)

    async def handle_core_output(self, time: float, words: list[str]) -> list[str]:
        return words
