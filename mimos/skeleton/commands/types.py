from abc import ABC


class Command(ABC):
    pass


class Act(Command):
    def __init__(self, animation_name: str):
        self.animation_name = animation_name


class Speak(Command):
    def __init__(self, text: str):
        self.text = text


class Do(Command):
    def __init__(self, *args: Command, parallel: bool = False):
        self.commands = args
        self.parallel = parallel
