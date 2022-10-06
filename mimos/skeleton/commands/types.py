from abc import ABC
from collections import defaultdict
from typing import Iterable
from mimos import config


class Command(ABC):
    pass


class Animate(Command):
    def __init__(self, animation_name: str):
        self.animation_name = animation_name


class Speak(Command):
    def __init__(self, text: str):
        self.text = text


class SequentialCommand(Command):
    def __init__(self, *args: Command):
        self.commands = args

    def __iter__(self):
        for command in self.commands:
            yield command

    def __index__(self, idx):
        return self.commands[idx]


class ParallelCommand(Command):
    def __init__(self, *args: Command):
        if len(args) > config.executors.num_parallel:
            raise Exception(
                "maximum number of commands that can be run parallely is",
                config.executors.num_parallel,
            )

        for arg in args:
            if type(arg) == ParallelCommand:
                raise Exception("parallel commands cannot be nested")

        self.check_animate(args)
        self.commands = args

    def __iter__(self):
        for command in self.commands:
            yield command

    def __index__(self, idx):
        return self.commands[idx]

    def check_animate(self, l: Iterable):
        data = defaultdict(lambda: 0)

        def count_cmds(l: Iterable):
            for i in l:
                if type(i) in [SequentialCommand, ParallelCommand]:
                    count_cmds(i)

                data[type[i]] += 1

        if data[Animate] > 1 or data[Speak] > 1:
            raise Exception(
                "animate and speak commands cannot be run in parallel with themselves"
            )
