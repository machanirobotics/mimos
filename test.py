import cv2
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
        while True:
            frame = cv2.imread("assets/pose4.png")
            self.frame_count += 1
            output = get_pose_keypoints(frame)
            image = output["frame"]
            keypoints = output["keypoints"]
            body.move(
                data=parse_obj_as(
                    FrameData, {"frame_number": self.frame_count, "angles": keypoints}
                )
            )
            # cv2.imshow("MediaPipe Holistic", image)
            # if cv2.waitKey(5) & 0xFF == 27:
            #     break

    # cv2.destroyAllWindows()


humanoid = mi.Humanoid(body=body, controller=Mimic())
humanoid.run()
