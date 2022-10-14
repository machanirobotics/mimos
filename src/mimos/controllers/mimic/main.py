import json
import math
import cv2
import numpy as np
import mediapipe as mp
from .translate import (
    ConvertPixelPointToBlenderUnits,
    get_angle,
    get_euler_angles,
    keypoint_joint_map,
)

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    static_image_mode=True,
    min_detection_confidence=0.7,
)

# read bonemap config
f = open("src/mimos/controllers/mimic/mimic.config.json")
mimic_config = json.load(f)

mimic_pose_landmarks = mimic_config["pose_landmarks"]
landmark_bone_map = mimic_config["landmark_bone_map"]


def translate_to_blender(
    joint_name: str,
    keypoint_dict: list,
    distanceBetweenEars,
):
    rotation_value = 0, 0, 0
    if joint_name in {"R_Shoulder", "L_Shoulder"}:
        joint_info = keypoint_joint_map[joint_name]
        # print(f"joint_name: {joint_name}")  # " joint_info: {joint_info}")

        kp1, kp2 = [
            ConvertPixelPointToBlenderUnits(
                np.array(keypoint_dict[joint]), distanceBetweenEars
            )
            for joint in joint_info["euler"]
        ]
        # print(f"kp1: {kp1}, kp2:{kp2}")
        rotation_value = get_euler_angles(kp1, kp2)
        print("rotation_value: ", rotation_value)
    return rotation_value


def mimic_frame(frame):
    frame.flags.writeable = False
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame)
    keypoint_dict = {}

    pose_landmarks = results.pose_landmarks

    if pose_landmarks is not None:
        pose_keypoints = pose_landmarks.landmark
        for idx in range(len(pose_keypoints)):
            keypoint = pose_keypoints[idx]
            landmark = mimic_pose_landmarks[idx]
            # passing only arm values
            if landmark in landmark_bone_map.keys():
                bone_name = landmark_bone_map[landmark]
                keypoint_dict[bone_name] = [keypoint.x, keypoint.y, keypoint.z]

    # # translate keypoints
    for joint, keypoint in keypoint_dict.items():
        keypoint_dict[joint] = translate_to_blender(joint, keypoint_dict, 0.17)

    mp_drawing.draw_landmarks(
        frame,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style(),
    )
    return frame, keypoint_dict
