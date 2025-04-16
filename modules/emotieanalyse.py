import cv2
from deepface import DeepFace

result_text = ""

def analyse_emotion(frame):
    global result_text

    try:
        
        results = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)

       
        if isinstance(results, list):
            emotion = results[0]['dominant_emotion']
        else:
            emotion = results['dominant_emotion']

       
        result_text = f"Emotion: {emotion}"
        cv2.putText(frame, result_text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    except Exception as e:
        result_text = "Geen gezicht gevonden"
        cv2.putText(frame, result_text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    return frame

def get_result():
    return result_text
