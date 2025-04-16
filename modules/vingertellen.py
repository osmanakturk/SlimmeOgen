

import cv2
import mediapipe as mp


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles


finger_count_global = 0

def count_fingers(frame):
    global finger_count_global

    with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=4, 
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    ) as hands:

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        total_count = 0

        if results.multi_hand_landmarks and results.multi_handedness:
            for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
                handedness = results.multi_handedness[i].classification[0].label 

              
                tips = [4, 8, 12, 16, 20]
                count = 0

            
                if is_thumb_open(hand_landmarks, handedness):
                    count += 1
                    draw_tip(frame, hand_landmarks, 4)

             
                for tip in tips[1:]:
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

                total_count += count

    
        cv2.putText(frame, f'Totaal: {total_count}', (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)

        finger_count_global = total_count
        return frame


def is_thumb_open(hand_landmarks, handedness):
    thumb_tip = 4
    thumb_ip = 3

    x_tip = hand_landmarks.landmark[thumb_tip].x
    x_ip = hand_landmarks.landmark[thumb_ip].x

    if handedness == "Right":
        return x_tip < x_ip  
    else:
        return x_tip > x_ip 


def draw_tip(frame, landmarks, index):
    h, w, _ = frame.shape
    x = int(landmarks.landmark[index].x * w)
    y = int(landmarks.landmark[index].y * h)
    cv2.circle(frame, (x, y), 12, (0, 0, 255), -1) 


def get_finger_count():
    global finger_count_global
    return finger_count_global
