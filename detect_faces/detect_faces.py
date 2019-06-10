import os
import numpy as np
import cv2

prototxt = os.path.join(os.getcwd(), 'detect_faces/deploy.prototxt.txt')
model = os.path.join(os.getcwd(), 'detect_faces/res10_300x300_ssd_iter_140000.caffemodel')

net = cv2.dnn.readNetFromCaffe(prototxt, model)

def detect(image):
    image_bytes = image.read()
    image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0,
                    (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()
    confidence = detections[0, 0, 0, 2]

    return True if confidence > 0.5 else False
            