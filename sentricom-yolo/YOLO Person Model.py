import sys
import argparse
from pathlib import Path
from ultralytics import YOLO

def main():
    # Count people in an image using YOLOv8"
    YOLO_parser = argparse.ArgumentParser()

    # Image file path (hardcoded)
    image_path = Path("test_image.webp")

    # Confidence threshold: between 0.0 – 1.0 (lower means more accurate but more false positives)
    YOLO_parser.add_argument("--threshold", type=float, default=0.25,)
    
    # Default can be changed to: yolov8n.pt, yolov8s.pt, yolov8m.pt
    # Model size definitions: n=fastest, s=balanced, m=most accurate.
    YOLO_parser.add_argument("--model", default="yolov8s.pt")
    args = YOLO_parser.parse_args()

    # Validate image path, if no image found
    if not image_path.exists():
        print(f"Error: image not found at '{image_path}'")
        sys.exit(1)

    # Load model and run inference
    model = YOLO(args.model)
    results = model(str(image_path), verbose=False)[0]

    # Filter to 'person' class only (COCO class ID 0) above threshold
    people = [
        box for box in results.boxes
        if int(box.cls.item()) == 0 and float(box.conf.item()) >= args.threshold
    ]

    # Count the number of people detected and calculate average confidence
    count = len(people)
    avgerage_confidence = sum(float(b.conf.item()) for b in people) / count if count > 0 else 0.0

    # Results
    print(f" \nPeople detected : {count}")
    print(f"Avg confidence  : {avgerage_confidence * 100:.1f}%")
    print("-" * 40)

    # Print confidence levels for each detected person
    if count > 0:
        print("\nDetection breakdown:")
        for i, box in enumerate(people, 1):
            conf = float(box.conf.item()) * 100
            print(f"  Person {i}: Confidence Level - {conf:.1f}%")


if __name__ == "__main__":
    main()