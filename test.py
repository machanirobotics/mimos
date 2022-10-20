import cv2
import mimos as mi
from pydantic import parse_obj_as
from mimos.skeleton.base import FrameData
from mimos.controllers import get_pose_keypoints

body = mi.Body(
    skeleton=mi.skeleton.Blender("blendfiles/Ria.blend", debug=True),
)

# run animation
# body.animate("namaste")

# pass custom values
# body.move(
#     data=parse_obj_as(
#         FrameData,
#         {
#             "frame_number": 1,
#             "angles": {
#                 "L_Shoulder": [
#                     0.30220987902160745,
#                     0.5990766108580907,
#                     -1.7778521865202142,
#                 ],
#             },
#         },
#     )
# )


# to pass custom joint angles to a joint
# while True:
#     try:
#         body.move(
#             data=parse_obj_as(
#                 FrameData,
#                 {
#                     "frame_number": 1,
#                     "angles": {
#                         "L_Shoulder": [
#                             0.30220987902160745,
#                             0.5990766108580907,
#                             -1.7778521865202142,
#                         ],
#                     },
#                 },
#             )
#         )
#     except KeyboardInterrupt:
#         break


class Mimic:
    def __init__(self):
        self.frame_count = 0

    def __call__(self, body):
        cap = cv2.VideoCapture("./assets/gym.mp4")
        while True:
            # frame = cv2.imread("assets/pose4.png")
            ret, frame = cap.read()
            if ret == True:
                self.frame_count += 1
                output = get_pose_keypoints(frame)
                image = output["frame"]
                keypoints = output["keypoints"]
                body.move(
                    data=parse_obj_as(
                        FrameData,
                        {"frame_number": self.frame_count, "angles": keypoints},
                    )
                )
                cv2.imshow("MediaPipe Holistic", image)
                if cv2.waitKey(5) & 0xFF == 27:
                    break
            else:
                break
        cap.release()
        cv2.destroyAllWindows()


# create humanoid object, pass on mimic controller
humanoid = mi.Humanoid(body=body, controller=Mimic())
humanoid.run()
