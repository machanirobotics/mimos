from mimos.skeleton.commands.types import (
    Animate,
    Command,
    ParallelCommand,
    SequentialCommand,
    Speak,
)
from mimos.utils import visitor
from mimos.skeleton.base import Skeleton, AnimationData
import mimos.config as config
import threading
import os
import toml
from pydantic import parse_obj_as


@visitor(match_first_n=1)
def execute():
    pass


@execute.case(Animate, Skeleton)
def execute_animation(command: Animate, skeleton: Skeleton):
    animation_name = command.animation_name
    file_name = f"{animation_name.lower()}.toml"
    animation_dir = config.executors.animation_dir
    if file_name not in os.listdir(animation_dir):
        raise Exception(f"Animation {animation_name} not found in {animation_dir}")
    res = toml.load(os.path.join(animation_dir, file_name))
    res = parse_obj_as(AnimationData, res)

    for frame in res.frames:
        skeleton.move(frame)


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
