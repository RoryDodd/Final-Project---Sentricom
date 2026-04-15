import sys
import argparse
from pathlib import Path
from ultralytics import YOLO
import json
import random
import math

def laplace_noise(scale):
    u = random.random() - 0.5
    return -scale * math.copysign(1, u) * math.log(1 - 2 * abs(u))

def classify(c):
    if c > 50:
        return "EVACUATE"
    elif c >= 25:
        return "MONITOR"
    else:
        return "LOW RISK"

def main():
    parser = argparse.ArgumentParser()

    image_dir = Path("images")

    parser.add_argument("--threshold", type=float, default=0.30)
    parser.add_argument("--epsilon", type=float, default=1.0)
    parser.add_argument("--model", default="yolov8s.pt")

    args = parser.parse_args()

    print("Looking in:", image_dir.resolve())
    print("Files found:", list(image_dir.glob("*")))

    model = YOLO(args.model)

    output = []

    for image_path in image_dir.glob("*"):
        if image_path.suffix.lower() not in [".jpg", ".jpeg", ".png", ".bmp", ".webp"]:
            continue

        if not image_path.exists():
            print(f"Error: image not found at '{image_path}'")
            continue

        print(f"\nProcessing: {image_path.name}")

        results = model(str(image_path), verbose=False)[0]

        people = [
            box for box in results.boxes
            if int(box.cls.item()) == 0 and float(box.conf.item()) >= args.threshold
        ]

        count = len(people)

        # Differential Privacy
        sensitivity = 1
        epsilon = args.epsilon

        if epsilon <= 0:
            print("Error: Epsilon must be greater than 0")
            sys.exit(1)

        scale = sensitivity / epsilon
        noise = laplace_noise(scale)
        noisy_count = max(0, round(count + noise))

        average_confidence = (
            sum(float(b.conf.item()) for b in people) / count if count > 0 else 0.0
        )

        error = abs(noisy_count - count)

        true_decision = classify(count)
        noisy_decision = classify(noisy_count)

        detections = [
            {
                "person_id": i + 1,
                "confidence": float(box.conf.item())
            }
            for i, box in enumerate(people)
        ]

        result_obj = {
            "image": image_path.name,
            "true_count": count,
            "noisy_count": noisy_count,
            "noise": round(noise, 3),
            "error": error,
            "average_confidence": round(average_confidence, 3),
            "true_decision": true_decision,
            "noisy_decision": noisy_decision,
            "decision_match": true_decision == noisy_decision,
            "detections": detections
        }

        output.append(result_obj)

    return {
        "epsilon": args.epsilon,
        "threshold": args.threshold,
        "model": args.model,
        "total_images": len(output),
        "results": output
    }


if __name__ == "__main__":
    results = main()

    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\nResults saved to results.json")