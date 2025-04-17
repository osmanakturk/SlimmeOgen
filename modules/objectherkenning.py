import cv2


PROTOTXT_PATH = "models/MobileNetSSD_deploy.prototxt"
MODEL_PATH = "models/MobileNetSSD_deploy.caffemodel"
LABELS_PATH = "models/MobileNetSSD.txt"


with open(LABELS_PATH, "r") as f:
    CLASSES = f.read().strip().split("\n")


COLORS = [(0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255)]


net = cv2.dnn.readNetFromCaffe(PROTOTXT_PATH, MODEL_PATH)

result_text = ""

def detect_objects(frame):
    global result_text

    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()

    objects = []

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        if confidence > 0.5:
            idx = int(detections[0, 0, i, 1])
            label = CLASSES[idx] if idx < len(CLASSES) else "Onbekend"
            box = detections[0, 0, i, 3:7] * [w, h, w, h]
            (startX, startY, endX, endY) = box.astype("int")

            cv2.rectangle(frame, (startX, startY), (endX, endY), COLORS[idx % len(COLORS)], 2)
            cv2.putText(frame, label, (startX, startY - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx % len(COLORS)], 2)

            objects.append(label)

    result_text = ", ".join(objects) if objects else "Geen objecten gevonden"
    return frame

def get_result():
    return result_text
