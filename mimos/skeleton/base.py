from abc import ABC, abstractmethod


class Skeleton(ABC):
    @abstractmethod
    def move(**kwargs):
        pass
