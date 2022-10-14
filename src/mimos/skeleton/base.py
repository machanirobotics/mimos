from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import List, Dict, Tuple
import numpy as np


class MimicData(BaseModel):
    """
    This class is used to represent mimic controllers output
    """

    frame: np.ndarray
    keypoint: Dict[str, List[float]]

    class Config:
        arbitrary_types_allowed = True


class FrameData(BaseModel):
    """
    This class is used to represent a frame in the animation.
    """

    frame_number: int
    angles: Dict[str, Tuple[float, float, float]]


class AnimationData(BaseModel):
    """
    This class is used to represent an animation.
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
