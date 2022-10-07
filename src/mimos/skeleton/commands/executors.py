from mimos.skeleton.commands.types import (
    Animate,
    Command,
    ParallelCommand,
    SequentialCommand,
    Speak,
)
from mimos.utils import visitor
from mimos.skeleton.base import Skeleton

import threading


@visitor(match_first_n=1)
def execute():
    pass


@execute.case(Animate, Skeleton)
def execute_animation(command: Animate, skeleton: Skeleton):
    pass


@execute.case(Speak, Skeleton)
def execute_speach(command: Speak, skeleton: Skeleton):
    pass


@execute.case(SequentialCommand, Skeleton)
def execute_sequentially(commands: SequentialCommand, skeleton: Skeleton):
    for command in commands:
        execute(command, skeleton)


@execute.case(ParallelCommand, Skeleton)
def execute_parallelly(commands: ParallelCommand, skeleton: Skeleton):
    def thread_func(command: Command, skeleton: Skeleton, barrier: threading.Barrier):
        execute(command, skeleton)
        barrier.wait()

    barrier = threading.Barrier(len(commands) + 1)
    for cmd in commands:
        threading.Thread(target=thread_func, args=(cmd, skeleton, barrier)).start()

    barrier.wait()


__all__ = ["execute"]
