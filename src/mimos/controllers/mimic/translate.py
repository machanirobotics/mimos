import math
import numpy as np


def translate_to_blender(
    joint_name: str, keypoint_dict: list, keypoint_joint_map: dict
):
    rotation_value = 0, 0, 0
    if joint_name in {"R_Shoulder", "L_Shoulder", "L_Elbow", "R_Elbow"}:
        joint_info = keypoint_joint_map[joint_name]

        kp1, kp2, kp3 = [
            ConvertPixelPointToBlenderUnits(np.array(keypoint_dict[joint]))
            for joint in joint_info["euler"]
        ]
        left = False if joint_name.startswith("R_") else True
        rotation_value = get_euler_angles(kp1, kp2, kp3, left)
    return rotation_value


def ConvertPixelPointToBlenderUnits(pnt, blender_scale=0.425):
    pntx = pnt[0] * blender_scale
    pnty = pnt[1] * blender_scale
    reliability = pnt[2] * blender_scale
    return [pntx, pnty, reliability]


def unit_vector(vector):
    """Returns them unit vector of the vector."""
    return vector / np.linalg.norm(vector)


def get_euler_angles(kp1: np.ndarray, kp2: np.ndarray, kp3: np.ndarray, left=False):
    if (
        isinstance(kp1, np.ndarray)
        and isinstance(kp2, np.ndarray)
        and isinstance(kp3, np.ndarray)
    ):
        uv1 = kp2 - kp1
        uv2 = kp3 - kp2
    else:
        uv1 = np.array(kp2) - np.array(kp1)
        uv2 = np.array(kp3) - np.array(kp2)
    square_uv1 = np.square(uv1)
    square_uv2 = np.square(uv2)

    denominator = math.sqrt(sum(square_uv1) * sum(square_uv2))
    blah = 0.0
    # if not left:
    #     blah = np.pi
    if not left:
        x_angle = np.arccos(uv1[0] * uv2[0] / denominator)  # * 180 / np.pi
        y_angle = np.arccos(uv1[1] * uv2[1] / denominator)  # * 180 / np.pi
        z_angle = np.arccos(uv1[2] * uv2[2] / denominator)  # * 180 / np.pi
    else:
        x_angle = np.pi - np.arccos(uv1[0] * uv2[0] / denominator)  # * 180 / np.pi
        y_angle = np.pi - np.arccos(uv1[1] * uv2[1] / denominator)  # * 180 / np.pi
        z_angle = np.pi - np.arccos(uv1[2] * uv2[2] / denominator)  # * 180 / np.pi
    return x_angle, y_angle, z_angle
