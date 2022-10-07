from typing import Optional
from mimos.skeleton import Skeleton
import mimos.skeleton.commands.executors as executor
from mimos.skeleton.commands.types import Animate, Command, SequentialCommand, Speak
from mimos.sensors.base import Input
from mimos.utils.channel import Rx, channel

import signal


class Body:
    def __init__(self, skeleton: Skeleton, vision: Optional[Input] = None):
        self.skeleton = skeleton
        self.vision = vision

        signal.signal(signal.SIGINT, lambda signal, frame: self.cleanup())

        if vision is not None:
            self.vision.start()

        self.is_cleaned_up = False

    def animate(self, animation: str):
        executor.execute(Animate(animation), self.skeleton)

    def speak(self, text: str):
        executor.execute(Speak(text), self.skeleton)

    def do(self, *args: Command):
        executor.execute(SequentialCommand(*args), self.skeleton)

    def move(self, **kwargs):
        self.skeleton.move(**kwargs)

    def see(self) -> Rx:
        if self.vision is None:
            raise Exception("no vision sensor attached to this body")
        tx, rx = channel(self.vision.queue_size)
        self.vision.register(tx)
        return rx

    def cleanup(self):
        if self.is_cleaned_up:
            return

        self.skeleton.destroy()
        self.stop_input_sensors()
        self.is_cleaned_up = True

    def stop_input_sensors(self):
        if self.vision is not None:
            self.vision.stop()

    def __del__(self):
        self.cleanup()
