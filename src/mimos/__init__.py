from .__version__ import __version__
from mimos.body import Body
from mimos.humanoid import Humanoid
from mimos.skeleton.commands import animate, speak, sequential, parallel
import mimos.skeleton as skeleton
import mimos.sensors as sensors
import mimos.controllers as controllers

__all__ = [
    "Body",
    "Humanoid",
    "animate",
    "speak",
    "sequential",
    "parallel",
    "skeleton",
    "sensors",
]
