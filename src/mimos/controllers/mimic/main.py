import cv2
import json
import mediapipe as mp
from .translate import translate_to_blender

# read bonemap config
f = open("src/mimos/controllers/mimic/config/mimic.config.json")
mimic_config = json.load(f)

mimic_pose_landmarks = mimic_config["pose_landmarks"]
landmark_bone_map = mimic_config["landmark_bone_map"]
keypoint_joint_map = mimic_config["keypoint_joint_map"]


def mediapipe_pose(frame):
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(
        static_image_mode=True,
        min_detection_confidence=0.7,
    )
    frame.flags.writeable = False
    results = pose.process(frame)
    pose_landmarks = results.pose_landmarks
    pose_world_landmarks = results.pose_world_landmarks

    return {
        "frame": frame,
        "pose_landmarks": pose_landmarks,
        "pose_world_landmarks": pose_world_landmarks,
    }


def get_pose_keypoints(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    keypoint_dict = {}

    # get mediapipe output
    mediapipe_output = mediapipe_pose(frame)
    output_frame = mediapipe_output["frame"]
    pose_landmarks = mediapipe_output["pose_landmarks"]
    pose_world_landmarks = mediapipe_output["pose_world_landmarks"]

    threed_coords = []
    if pose_landmarks is not None:
        pose_keypoints = pose_landmarks.landmark
        pose_world_keypoints = pose_world_landmarks.landmark
        for idx in range(len(pose_keypoints)):
            keypoint = pose_keypoints[idx]
            landmark = mimic_pose_landmarks[idx]

            # passing only arm values
            if landmark in landmark_bone_map.keys():
                bone_name = landmark_bone_map[landmark]
                # world coordinates
                world_keypoint = pose_world_keypoints[idx]
                threed_coords.append(
                    [world_keypoint.x, world_keypoint.y, world_keypoint.z]
                )
                keypoint_dict[bone_name] = [keypoint.x, keypoint.y, keypoint.z]

    # get translated angles
    for joint, keypoint in keypoint_dict.items():
        keypoint_dict[joint] = translate_to_blender(
            joint, keypoint_dict, keypoint_joint_map
        )

    return {"frame": output_frame, "keypoints": keypoint_dict}
