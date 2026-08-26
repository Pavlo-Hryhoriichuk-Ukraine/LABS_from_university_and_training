import numpy as np

def calculate_means(data: np.ndarray) -> tuple[float, float, float]:
    """
    Calculates the Arithmetic (AM), Geometric (GM), and Harmonic (HM) means.
    Input data must be a NumPy array of positive numbers (> 0).
    """
    # 1. Filter out zeros (log(0) or 1/0 will crash the program)
    valid_data = data[data > 0]

    if len(valid_data) == 0:
        raise ValueError("Data array is empty or contains only zeros.")

    am = float(np.mean(valid_data))

    gm = np.exp(np.mean(np.log(valid_data)))

    hm = len(valid_data) / np.sum(1.0 / valid_data)

    return am, gm, hm


def calculate_triangle_angles(am: float, gm: float, hm: float) -> tuple[float, float, float]:
    """
    Treats AM, GM, and HM as the lengths of three sides of a triangle.
    Calculates and returns the internal angles in degrees.
    """

    a, b, c = hm, gm, am

    if not (a + b > c and a + c > b and b + c > a):
        raise ValueError("Triangle Inequality violated! AM is too large compared to HM and GM.")

    cos_A = np.clip((b**2 + c**2 - a**2) / (2 * b * c), -1.0, 1.0)
    cos_B = np.clip((a**2 + c**2 - b**2) / (2 * a * c), -1.0, 1.0)
    cos_C = np.clip((a**2 + b**2 - c**2) / (2 * a * b), -1.0, 1.0)

    angle_A_rad = np.arccos(cos_A)
    angle_B_rad = np.arccos(cos_B)
    angle_C_rad = np.arccos(cos_C)

    angle_A_deg = np.degrees(angle_A_rad)
    angle_B_deg = np.degrees(angle_B_rad)
    angle_C_deg = np.degrees(angle_C_rad)

    return angle_A_deg, angle_B_deg, angle_C_deg