import cv2
import mediapipe as mp
import math


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles


hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,  
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)


finger_count_global = 0
result_text = ""

def count_fingers(frame):
    global finger_count_global, result_text

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    total_count = 0

    if results.multi_hand_landmarks and results.multi_handedness:
        hand_landmarks = results.multi_hand_landmarks[0]
        handedness = results.multi_handedness[0].classification[0].label 

        if is_fist(hand_landmarks):
            count = 0
        else:
            count = 0
            if is_thumb_open(hand_landmarks, handedness):
                count += 1
                draw_tip(frame, hand_landmarks, 4)

            tips = [8, 12, 16, 20]
            for tip in tips:
                if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
                    count += 1
                    draw_tip(frame, hand_landmarks, tip)

        mp_drawing.draw_landmarks(
            frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style()
        )

        h, w, _ = frame.shape
        cx = int(hand_landmarks.landmark[0].x * w)
        cy = int(hand_landmarks.landmark[0].y * h)
        cv2.putText(frame, f'{count} vingers ({handedness})', (cx, cy - 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

        total_count = count

    cv2.putText(frame, f'Totaal: {total_count}', (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)

    finger_count_global = total_count
    result_text = f"Vingers: {total_count}"
    return frame


def is_thumb_open(hand_landmarks, handedness):
    tip = hand_landmarks.landmark[4]
    ip = hand_landmarks.landmark[3]
    mcp = hand_landmarks.landmark[2]
    cmc = hand_landmarks.landmark[1]
    wrist = hand_landmarks.landmark[0]
    index_mcp = hand_landmarks.landmark[5]

  
    palm_outward = wrist.z > index_mcp.z  

    v1 = [ip.x - mcp.x, ip.y - mcp.y, ip.z - mcp.z]
    v2 = [tip.x - ip.x, tip.y - ip.y, tip.z - ip.z]

    dot = sum(a * b for a, b in zip(v1, v2))
    mag1 = math.sqrt(sum(a * a for a in v1))
    mag2 = math.sqrt(sum(a * a for a in v2))
    angle = math.acos(dot / (mag1 * mag2)) if mag1 and mag2 else 0
    angle_deg = math.degrees(angle)

    
    z_diff = mcp.z - tip.z  

 
    if palm_outward:
        return z_diff > 0.02 and angle_deg < 50
    else:
        return z_diff < -0.02 and angle_deg < 50



def is_fist(hand_landmarks):
    finger_tips = [8, 12, 16, 20]
    finger_pips = [6, 10, 14, 18]

    closed = 0
    for tip, pip in zip(finger_tips, finger_pips):
        if hand_landmarks.landmark[tip].y > hand_landmarks.landmark[pip].y:
            closed += 1

    return closed >= 4 

def draw_tip(frame, landmarks, index):
    h, w, _ = frame.shape
    x = int(landmarks.landmark[index].x * w)
    y = int(landmarks.landmark[index].y * h)
    cv2.circle(frame, (x, y), 12, (0, 0, 255), -1)

def get_finger_count():
    return finger_count_global

def get_result():
    return result_text
