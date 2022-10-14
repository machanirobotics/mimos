from array import array


def CombineRReliability(pt1: array, pt2: array):
    """
    Returns combined reliability of two keypoint value
    """
    rel1 = pt1[2]
    rel2 = pt2[2]
    if rel1 < rel2:
        relOut = rel1
    else:
        relOut = rel2
    return relOut


def GetPoint(KeypointArray: array, index: int):
    """
    Returns keypoint value of input array by index
    """
    baseIndex = index
    x = float(KeypointArray[baseIndex][0])
    y = float(KeypointArray[baseIndex][1])
    reliability = float(KeypointArray[baseIndex][2])
    return [x, y, reliability]


def AverageTwoPoints(pt1: array, pt2: array):
    """
    Returns average of two keypoint value
    """
    avgX = (pt1[0] + pt2[0]) / 2
    avgY = (pt1[1] + pt2[1]) / 2
    return [avgX, avgY, CombineRReliability(pt1, pt2)]


def DifferenceBetweenPoint(pt1: array, pt2: array):
    """
    Returns difference between two keypoint value
    """
    diffX = pt1[0] - pt2[0]
    diffY = pt1[1] - pt2[1]
    return [diffX, diffY, CombineRReliability(pt1, pt2)]


def Multiply(pt: array, val: int):
    """
    Returns multiplied keypoint value with correction factor
    """
    x = pt[0] * val
    y = pt[1] * val
    return [x, y, pt[2]]
