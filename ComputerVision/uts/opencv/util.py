import numpy as np
import cv2 

def get_limits(color, loose=False):
    c = np.uint8([[color]])
    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)
    hue = int(hsvC[0][0][0])

    s_min = 30 if loose else 100
    v_min = 30 if loose else 100
    hue_range = 15 if loose else 10   # wider range for tricky colors

    if hue >= 170 or hue <= 10:
        lower_limit1 = np.array([0,   s_min, v_min], dtype=np.uint8)
        upper_limit1 = np.array([10,  255,   255  ], dtype=np.uint8)
        lower_limit2 = np.array([170, s_min, v_min], dtype=np.uint8)
        upper_limit2 = np.array([179, 255,   255  ], dtype=np.uint8)
        return [(lower_limit1, upper_limit1), (lower_limit2, upper_limit2)]

    lower_limit = np.array([max(0,   hue - hue_range), s_min, v_min], dtype=np.uint8)
    upper_limit = np.array([min(179, hue + hue_range), 255,   255  ], dtype=np.uint8)
    return [(lower_limit, upper_limit)]


def get_combined_mask(hsv_frame, colors, loose=False):
    mask = None
    for color in colors:
        for lower, upper in get_limits(color, loose=loose):
            part = cv2.inRange(hsv_frame, lower, upper)
            mask = part if mask is None else cv2.bitwise_or(mask, part)
    return mask