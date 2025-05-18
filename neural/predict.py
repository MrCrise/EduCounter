import cv2
import numpy as np
from ultralytics import YOLO
from neural_config import *


model = YOLO(MODEL_PATH)


def model_predict(frame: any) -> int:
    '''
    Runs YOLO inference on a given frame and returns count of people on it.
    '''

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    prediction = model.predict(
        source=rgb_frame,
        device=MODEL_DEVICE,
        classes=MODEL_CLASSES,
        save=MODEL_SAVE,
        project=MODEL_PROJECT,
        imgsz=MODEL_IMGSZ,
        )

    detections: list = prediction[0]

    people_count: int = len(detections)

    return people_count
