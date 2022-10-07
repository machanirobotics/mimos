from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import List, Dict, Tuple


class FrameData(BaseModel):
    """
    This class is used to represent a frame in the animation.

    Args:
        BaseModel (_type_): pydantic model.
    """

    frame_number: int
    angles: Dict[str, Tuple[float, float, float]]


class AnimationData(BaseModel):
    """
    This class is used to represent an animation.

    Args:
        BaseModel (_type_): pydantic model.
    """

    action: str
    start_frame: int
    end_frame: int
    frames: List[FrameData]


class Skeleton(ABC):
    @abstractmethod
    def move(data: FrameData):
        pass

    @abstractmethod
    def destroy(self):
        pass
