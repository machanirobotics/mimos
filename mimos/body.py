from mimos.skeleton import Skeleton
import mimos.skeleton.commands.executors as executor
from mimos.skeleton.commands.types import Animate, Command, SequentialCommand, Speak


class Body:
    def __init__(self, skeleton: Skeleton):
        self.skeleton = skeleton

    def animate(self, animation: str):
        executor.execute(Animate(animation), self.skeleton)

    def speak(self, text: str):
        executor.execute(Speak(text), self.skeleton)

    def do(self, *args: Command):
        executor.execute(SequentialCommand(*args), self.skeleton)

    def move(self, **kwargs):
        self.skeleton.move(**kwargs)
