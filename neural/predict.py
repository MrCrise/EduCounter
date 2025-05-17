import torch
import cv2
import numpy as np
from neural_config import MODEL_PATH


model = torch.hub.load(
    source='local',
    repo_or_dir=MODEL_PATH,
    )


def model_predict(frame: any) -> int:
    '''
    Runs YOLO inference on a given frame and returns count of people on it.
    Assume 'person' class index is 0.

    TODO: Implement support of YOLOv11 model, current
          realisation only support old YOLO models.
    '''

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    prediction = model(rgb_frame)

    detections: np.ndarray = prediction.xyxy[0].cpu().numpy()

    # Select every detection where class id is 0 and find count.
    people_count: int = int((detections[:, 5] == 0).sum())

    return people_count
