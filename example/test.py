import cv2
import numpy as np
import mimos as mi
from pydantic import parse_obj_as
from mimos.skeleton.base import FrameData
from mimos.controllers import get_pose_keypoints

body = mi.Body(
    skeleton=mi.skeleton.Blender(
        "/home/rohan/Desktop/mrobotics/mimos/blendfiles/Ria.blend", debug=True
    ),
)


class Mimic:
    def __init__(self):
        self.frame_count = 0

    def __call__(self, body):
        # for frame in body.see():
        while True:
            frame = cv2.imread("assets/pose10.jpg")
            self.frame_count += 1
            image, keypoints = get_pose_keypoints(frame)
            body.move(
                data=parse_obj_as(
                    FrameData, {"frame_number": self.frame_count, "angles": keypoints}
                )
            )
            cv2.imshow("MediaPipe Holistic", cv2.flip(image, 1))
            if cv2.waitKey(5) & 0xFF == 27:
                break

    cv2.destroyAllWindows()


humanoid = mi.Humanoid(body=body, controller=Mimic())
humanoid.run()
