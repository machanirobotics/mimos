import numpy as np
import math


def get_euler_angles(kp1: np.ndarray, kp2: np.ndarray):
    if isinstance(kp1, np.ndarray) and isinstance(kp2, np.ndarray):
        uv = np.subtract(kp2, kp1)
    else:
        uv = np.array(kp2) - np.array(kp1)
    square_uv = np.square(uv)

    denominator = math.sqrt(np.sum(square_uv))
    x_angle = np.arccos(uv[0] / denominator)  # * 180 / np.pi
    y_angle = np.arccos(uv[1] / denominator)  # * 180 / np.pi
    z_angle = np.arccos(uv[2] / denominator)  # * 180 / np.pi
    # switching z with y because of blender model is on x+90
    return x_angle, y_angle, z_angle


0
