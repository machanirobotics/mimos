from typing import Optional
from mimos.sensors.base import Input
import cv2
import time


class RGBCamera(Input):
    def __init__(
        self,
        id: Optional[int] = 0,
        fps: Optional[int] = 30,
        max_buffers: Optional[int] = None,
    ):
        super().__init__(queue_size=max_buffers)
        self.cam = cv2.VideoCapture(id)
        self.fps = fps
        self.prev_time = 0

    def get_data(self):
        now = time.time()
        _, frame = self.cam.read()

        if now - self.prev_time > 1.0 / self.fps:
            self.prev_time = now
            return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
