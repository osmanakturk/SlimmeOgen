import cv2
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_drawing = mp.solutions.drawing_utils


canvas = None
prev_x, prev_y = None, None

def bewegend_tekenen(frame):
    global canvas, prev_x, prev_y

    h, w, _ = frame.shape

    # İlk karede canvas oluştur
    if canvas is None:
        canvas = np.zeros_like(frame)

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]

       
        index_finger = hand_landmarks.landmark[8]
        x, y = int(index_finger.x * w), int(index_finger.y * h)

        
        if prev_x is not None and prev_y is not None:
            cv2.line(canvas, (prev_x, prev_y), (x, y), (0, 0, 155), 5)

        prev_x, prev_y = x, y

     
        cv2.circle(frame, (x, y), 8, (0, 255, 0), -1)

      
        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    else:
        prev_x, prev_y = None, None 

   
    combined = cv2.addWeighted(frame, 1, canvas, 1, 0)

    return combined
