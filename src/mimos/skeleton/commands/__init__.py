from mimos.skeleton.commands.types import (
    Animate,
    Command,
    Speak,
    SequentialCommand,
    ParallelCommand,
)


def animate(animation: str):
    return Animate(animation)


def speak(text: str):
    return Speak(text)


def sequential(*args: Command):
    return SequentialCommand(*args)


def parallel(*args: Command):
    return ParallelCommand(*args)


__all__ = ["animate", "speak", "sequential", "parallel"]
