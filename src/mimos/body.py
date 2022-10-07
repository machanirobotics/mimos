from mimos.skeleton import Skeleton
import mimos.skeleton.commands.executors as executor
from mimos.skeleton.commands.types import Animate, Command, SequentialCommand, Speak
from mimos.sensors.base import Input
from mimos.utils.channel import Rx, channel

import signal


class Body:
    def __init__(self, skeleton: Skeleton, vision: Input):
        self.skeleton = skeleton
        self.vision = vision

        signal.signal(signal.SIGINT, lambda signal, frame: self.stop_input_sensors())

        self.vision.start()

    def animate(self, animation: str):
        executor.execute(Animate(animation), self.skeleton)

    def speak(self, text: str):
        executor.execute(Speak(text), self.skeleton)

    def do(self, *args: Command):
        executor.execute(SequentialCommand(*args), self.skeleton)

    def move(self, **kwargs):
        self.skeleton.move(**kwargs)

    def see(self) -> Rx:
        tx, rx = channel(self.vision.queue_size)
        self.vision.register(tx)
        return rx

    def stop_input_sensors(self):
        self.vision.stop()
