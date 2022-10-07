from abc import ABC, abstractmethod


class JointData:
    pass


class Skeleton(ABC):
    @abstractmethod
    def move(data: JointData):
        pass
