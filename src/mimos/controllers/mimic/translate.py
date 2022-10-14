import numpy as np
import math

LeftRightEarlobeDistance = 1.74095
distanceBetweenEars = 0
keypoint_joint_map = {
    "R_Shoulder": {
        "id": 2,
        "scale": 1,
        "axis": "y",
        "euler": ["R_Shoulder", "R_Elbow"],
    },
    "R_Elbow": {
        "id": 3,
        "scale": 1,
        "axis": "z",
        "euler": ["R_Elbow", "R_Wrist"],
    },
    "R_Wrist": {"id": 4, "scale": -1, "axis": "x", "euler": ["R_Elbow", "R_Wrist"]},
    "L_Shoulder": {
        "id": 5,
        "scale": 1,
        "axis": "y",
        "euler": ["L_Shoulder", "L_Elbow"],
    },
    "L_Elbow": {
        "id": 6,
        "scale": 1,
        "axis": "z",
        "euler": ["L_Elbow", "L_Wrist"],
    },
    "L_Wrist": {"id": 7, "scale": -1, "axis": "x", "euler": ["L_Elbow", "L_Wrist"]},
}


def ConvertPixelPointToBlenderUnits(pnt, distanceBetweenEars):
    pntx = pnt[0]  # * (LeftRightEarlobeDistance / (distanceBetweenEars + 1e-6))
    pnty = pnt[1]  # * (LeftRightEarlobeDistance / (distanceBetweenEars + 1e-6))
    reliability = pnt[2]
    return [pntx, pnty, reliability]


def unit_vector(vector):
    """Returns the unit vector of the vector."""
    return vector / np.linalg.norm(vector)


def get_angle(k1: np.ndarray, k2: np.ndarray, k3: np.ndarray):
    """
    the keypoints k1, k2, k3 are connected in this order, and the result angle (IN DEGREES) is the angle at joint k2
        ki = (xi, yi); each keypoint is a np array of x and y coords
    """
    v1 = np.subtract(k2, k1)
    v2 = np.subtract(k3, k2)
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.dot(v1_u, v2_u)) * 180.0 / np.pi


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
