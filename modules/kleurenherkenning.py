
import cv2
import numpy as np

result_text = ""


def detect_color(frame):
    global result_text
    h, w, _ = frame.shape
    cx, cy = w // 2, h // 2
    size = 50
    roi = frame[cy-size:cy+size, cx-size:cx+size]


    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    avg_hsv = cv2.mean(hsv_roi)[:3] 

    color_name = classify_color(avg_hsv)
    result_text = f"Kleur: {color_name}"

    cv2.rectangle(frame, (cx - size, cy - size), (cx + size, cy + size), (0, 255, 255), 2)


    cv2.putText(frame, f'Kleur: {color_name}', (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

    return frame

def classify_color(hsv):
    h, s, v = hsv


    if v < 50:
        return "Zwart"
    if s < 40 and v >= 200:
        return "Wit"
    if s < 40 and v < 200:
        return "Grijs"


    if h < 15 or h >= 170:
        return "Rood"
    elif 15 <= h < 25:
        return "Oranje"
    elif 25 <= h < 35:
        return "Geel"
    elif 35 <= h < 85:
        return "Groen"
    elif 85 <= h < 125:
        return "Blauw"
    elif 125 <= h < 155:
        return "Paars"
    elif 155 <= h < 170:
        return "Roze"
    else:
        return "Onbekend"


def get_result():
    return result_text