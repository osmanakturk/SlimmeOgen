import cv2
import numpy as np


CONFIG_PATH = "models/yolov4-tiny.cfg"
WEIGHTS_PATH = "models/yolov4-tiny.weights"
NAMES_PATH = "models/coco.names"


with open(NAMES_PATH, 'r') as f:
    classes = [line.strip() for line in f.readlines()]


net = cv2.dnn.readNetFromDarknet(CONFIG_PATH, WEIGHTS_PATH)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)


detected_objects = ""

def detect_objects(frame):
    global detected_objects

    height, width = frame.shape[:2]

    
    blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)

    ln = net.getLayerNames()
    output_layers = [ln[i - 1] for i in net.getUnconnectedOutLayers().flatten()]

    layer_outputs = net.forward(output_layers)

    boxes = []
    confidences = []
    class_ids = []

   
    for output in layer_outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    detected_labels = []

    if len(indexes) > 0:
        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = confidences[i]
            detected_labels.append(label)

            color = (0, 255, 0)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, f"{label} {int(confidence * 100)}%", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    if detected_labels:
        detected_objects = ", ".join(detected_labels)
    else:
        detected_objects = "Geen objecten gedetecteerd"

    return frame


def get_result():
    return detected_objects
