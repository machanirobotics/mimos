import json
import numpy as np

blender_config = json.load(
    open("src/mimos/controllers/mimic/config/blender.config.json")
)


def translate_to_blender(
    joint_name: str, keypoint_dict: list, keypoint_joint_map: dict
):
    """
    translates keypoints to euler angles
    """
    rotation_value = 0, 0, 0
    if joint_name in {"R_Shoulder", "L_Shoulder", "L_Elbow", "R_Elbow"}:
        joint_info = keypoint_joint_map[joint_name]

        kp1, kp2, kp3 = [
            ConvertPixelPointToBlenderUnits(np.array(keypoint_dict[joint]))
            for joint in joint_info["euler"]
        ]
        left = False if joint_name.startswith("R_") else True
        bone_info = [
            bone_
            for bone_ in blender_config["bone_config"]
            if bone_["bone_name"] == joint_name
        ]
        joint_scale = bone_info[0]["scale"]
        rotation_value = get_euler_angles(kp1, kp2, kp3, left)
    return rotation_value


def ConvertPixelPointToBlenderUnits(pnt: np.ndarray, blender_scale=0.425) -> list:
    """
    converts pixel point to blender units
    """
    pntx = pnt[0] * blender_scale
    pnty = pnt[1] * blender_scale
    reliability = pnt[2] * blender_scale
    return [pntx, pnty, reliability]


def get_euler_angles(
    kp1: np.ndarray, kp2: np.ndarray, kp3: np.ndarray, left=False
) -> list:
    """
    calculates euler angles from keypoints
    """
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

    R = rotation_matrix_from_vectors(uv1, uv2)
    z_angle, y_angle, x_angle = Decompose_R_ZXY(R)
    z_angle = -z_angle
    y_angle = -y_angle
    return [x_angle, y_angle, z_angle]


def rotation_matrix_from_vectors(vec1: np.ndarray, vec2: np.ndarray) -> np.ndarray:
    """find the rotation matrix that aligns vec1 to vec2
    :param vec1: A 3d "source" vector
    :param vec2: A 3d "destination" vector
    :return mat: A transform matrix (3x3) which when applied to vec1, aligns it with vec2.
    """
    a, b = (vec1 / np.linalg.norm(vec1)).reshape(3), (
        vec2 / np.linalg.norm(vec2)
    ).reshape(3)
    v = np.cross(a, b)
    c = np.dot(a, b)
    s = np.linalg.norm(v)
    kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    rotation_matrix = np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s**2))
    return rotation_matrix


def Decompose_R_ZXY(R: np.ndarray) -> list:
    """
    decompose rotation matrix to euler angles in radians
    """
    thetaz = np.arctan2(-R[0, 1], R[1, 1])
    thetay = np.arctan2(-R[2, 0], R[2, 2])
    thetax = np.arctan2(R[2, 1], np.sqrt(R[2, 0] ** 2 + R[2, 2] ** 2))
    return thetaz, thetay, thetax
