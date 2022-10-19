import math
import numpy as np


def translate_to_blender(
    joint_name: str, keypoint_dict: list, keypoint_joint_map: dict
):
    rotation_value = 0, 0, 0
    if joint_name in {"R_Shoulder", "L_Shoulder", "L_Elbow", "R_Elbow"}:
        joint_info = keypoint_joint_map[joint_name]

        kp1, kp2 = [
            ConvertPixelPointToBlenderUnits(np.array(keypoint_dict[joint]))
            for joint in joint_info["euler"]
        ]
        rotation_value = get_euler_angles(kp1, kp2)
    return rotation_value


def ConvertPixelPointToBlenderUnits(pnt, blender_scale=0.425):
    pntx = pnt[0] * blender_scale
    pnty = pnt[1] * blender_scale
    reliability = pnt[2] * blender_scale
    return [pntx, pnty, reliability]


def unit_vector(vector):
    """Returns them unit vector of the vector."""
    return vector / np.linalg.norm(vector)


def get_euler_angles(kp1: np.ndarray, kp2: np.ndarray):
    if isinstance(kp1, np.ndarray) and isinstance(kp2, np.ndarray):
        uv = kp2 - kp1
    else:
        uv = np.array(kp2) - np.array(kp1)
    square_uv = np.square(uv)

    denominator = math.sqrt(sum(square_uv))
    x_angle = np.arccos(uv[0] / denominator)  # * 180 / np.pi
    y_angle = np.arccos(uv[1] / denominator)  # * 180 / np.pi
    z_angle = np.arccos(uv[2] / denominator)  # * 180 / np.pi
    return x_angle, y_angle, z_angle
