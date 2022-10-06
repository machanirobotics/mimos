from mimos.skeleton.commands.types import (
    Command,
    Animate,
    ParallelCommand,
    SequentialCommand,
    Speak,
)
from mimos.skeleton.utils import visitor
from mimos.skeleton.base import Skeleton


@visitor(match_first_n=1)
def execute():
    raise NotImplementedError("Do not call this directly")


@execute.case(Animate, Skeleton)
def execute_animation(command, skeleton):
    print("executing animation")


@execute.case(Speak, Skeleton)
def execute_speach(command, skeleton):
    print("executing speech")


@execute.case(SequentialCommand, Skeleton)
def execute_sequentially(commands, skeleton):
    print("executing sequential")
    for command in commands:
        execute(command, skeleton)


@execute.case(ParallelCommand, Skeleton)
def execute_parallelly(commands, skeleton):
    print("executing parallel")


__all__ = ["execute"]
