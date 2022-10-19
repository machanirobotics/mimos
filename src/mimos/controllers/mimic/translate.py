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

    # R = Get_R(uv1, uv2)
    R = rotation_matrix_from_vectors(uv1, uv2)
    z_angle, y_angle, x_angle = Decompose_R_ZXY(R)
    # square_uv1 = np.square(uv1)
    # square_uv2 = np.square(uv2)

    # denominator = math.sqrt(sum(square_uv1) * sum(square_uv2))
    # blah = 0.0
    # # if not left:
    # #     blah = np.pi
    # if not left:
    #     x_angle = np.arccos(uv1[0] * uv2[0] / denominator)  # * 180 / np.pi
    #     y_angle = np.arccos(uv1[1] * uv2[1] / denominator)  # * 180 / np.pi
    #     z_angle = np.arccos(uv1[2] * uv2[2] / denominator)  # * 180 / np.pi
    # else:
    #     x_angle = np.pi - np.arccos(uv1[0] * uv2[0] / denominator)  # * 180 / np.pi
    #     y_angle = np.pi - np.arccos(uv1[1] * uv2[1] / denominator)  # * 180 / np.pi
    #     z_angle = np.pi - np.arccos(uv1[2] * uv2[2] / denominator)  # * 180 / np.pi
    # if not left:
    #     x_angle = np.pi - x_angle
    # x_angle, y_angle, z_angle = 0.52, 0.52, 0.52
    # if not left:
    y_angle = -y_angle
    z_angle = -z_angle
    print(
        f"x, y, z angles - {x_angle*180./np.pi}, {y_angle*180./np.pi}, {z_angle*180./np.pi}"
    )
    return x_angle, y_angle, z_angle


def rotation_matrix_from_vectors(vec1, vec2):
    """Find the rotation matrix that aligns vec1 to vec2
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


# calculate rotation matrix to take A vector to B vector
def Get_R(A, B):

    # get unit vectors
    uA = A / np.sqrt(np.sum(np.square(A)))
    uB = B / np.sqrt(np.sum(np.square(B)))

    # get products
    cos_t = np.sum(uA * uB)
    sin_t = np.sqrt(np.sum(np.square(np.cross(uA, uB))))  # magnitude

    # get new unit vectors
    u = uA
    v = uB - np.sum(uA * uB) * uA
    v = v / np.sqrt(np.sum(np.square(v)))
    w = np.cross(uA, uB)
    w = w / np.sqrt(np.sum(np.square(w)))

    # get change of basis matrix
    C = np.array([u, v, w])

    # get rotation matrix in new basis
    R_uvw = np.array([[cos_t, -sin_t, 0], [sin_t, cos_t, 0], [0, 0, 1]])

    # full rotation matrix
    R = C.T @ R_uvw @ C
    # print(R)
    return R


def Decompose_R_ZXY(R):

    # decomposes as RzRXRy. Note the order: ZXY <- rotation by y first
    thetaz = np.arctan2(-R[0, 1], R[1, 1])
    thetay = np.arctan2(-R[2, 0], R[2, 2])
    thetax = np.arctan2(R[2, 1], np.sqrt(R[2, 0] ** 2 + R[2, 2] ** 2))

    return thetaz, thetay, thetax
