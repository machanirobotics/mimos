from mimos.skeleton.base import JointData, Skeleton


class Blender(Skeleton):
    def __init__(self):
        self.blend_file = ""

    def move(self, data: JointData):
        pass
