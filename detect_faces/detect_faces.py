import os
import numpy as np
import cv2

# path to the prototxt file
prototxt = os.path.join(os.getcwd(), 'detect_faces/deploy.prototxt.txt')
# path to the model file
model = os.path.join(os.getcwd(), 'detect_faces/res10_300x300_ssd_iter_140000.caffemodel')

# importing the face detection architecture from opencv
net = cv2.dnn.readNetFromCaffe(prototxt, model)

# function to detect the image
def detect(image):
    # getting the user inputs
    image_bytes = image.read()
    # converting the bytes array to image
    image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
    # extracting height and width from the image
    (h, w) = image.shape[:2]
    # setting the input for the dnn from the image
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0,
                    (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    # detecting the face
    detections = net.forward()
    #getting the confidence of the detection
    confidence = detections[0, 0, 0, 2]

    return True if confidence > 0.5 else False
            