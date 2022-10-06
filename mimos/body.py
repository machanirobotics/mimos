from mimos.skeleton import Skeleton
from mimos.skeleton.commands.types import Act, Command, Do, Speak


class Body:
    def __init__(self, skeleton: Skeleton):
        self.skeleton = skeleton

    def act(self, animation: str):
        self.act_impl(Act(animation))

    def speak(self, text: str):
        self.speak_impl(Speak(text))

    def do(self, *args: Command, parallel: bool = False):
        self.do_impl(Do(*args, parallel=parallel))

    def move(self, **kwargs):
        self.skeleton.move(**kwargs)

    def act_impl(self, command: Act):
        pass

    def speak_impl(self, command: Speak):
        raise NotImplementedError()

    def do_impl(self, command: Do):
        raise NotImplementedError()
