from .__version__ import __version__
from mimos.body import Body
from mimos.skeleton.commands import animate, speak, sequential, parallel
import mimos.skeleton as skeleton
import mimos.sensors as sensors

__all__ = ["Body", "animate", "speak", "sequential", "parallel", "skeleton", "sensors"]
