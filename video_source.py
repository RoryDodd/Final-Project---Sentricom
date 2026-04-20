from pathlib import Path
from ultralytics import YOLO
import cv2


class VideoSource:
    def __init__(self, video_path: Path, model_path: str, threshold: float, frame_skip: int):
        self.video_path = Path(video_path)
        self.model_path = model_path
        self.threshold = threshold
        self.frame_skip = frame_skip
        self.cap = None
        self.model = None

    def validate(self) -> None:
        if not self.video_path.exists():
            raise FileNotFoundError(f"Video not found at '{self.video_path}'")

    def open(self) -> None:
        self.validate()
        self.cap = cv2.VideoCapture(str(self.video_path))
        if not self.cap.isOpened():
            raise RuntimeError(f"Could not open video '{self.video_path}'")
        self.model = YOLO(self.model_path)

    def close(self) -> None:
        if self.cap is not None:
            self.cap.release()
            self.cap = None

    def get_properties(self):
        if self.cap is None:
            raise RuntimeError("Video capture is not open")
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        return fps, total_frames

    def frames(self):
        frame_count = 0
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            frame_count += 1
            if frame_count % self.frame_skip != 0:
                continue
            yield frame_count, frame

    def count_people(self, frame):
        results = self.model(frame, verbose=False)[0]
        people = [
            box for box in results.boxes
            if int(box.cls.item()) == 0 and float(box.conf.item()) >= self.threshold
        ]
        avg_conf = (
            sum(float(b.conf.item()) for b in people) / len(people) * 100
            if people else 0.0
        )
        return len(people), avg_conf
