import cv2
import pytesseract

# Windows
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Raspberry Pi
# pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

result_text = ""

def detect_text(frame):
    global result_text

  
    frame = cv2.flip(frame, 1)


    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

 
    text = pytesseract.image_to_string(thresh)
    result_text = text.strip()

    lines = result_text.split('\n')
    y_offset = frame.shape[0] - (30 * len(lines)) - 10

    for i, line in enumerate(lines):
        if line.strip():
            cv2.putText(frame, line, (10, y_offset + i * 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    return frame

def get_result():
    return result_text if result_text else "Geen tekst gedetecteerd"
