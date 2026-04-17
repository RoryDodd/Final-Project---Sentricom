import sys
import argparse
from pathlib import Path
import datetime

from dp import DifferentialPrivacy
from video_source import VideoSource


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--threshold", type=float, default=0.30)
    parser.add_argument("--epsilon", type=float, default=0.7)
    parser.add_argument("--frame_skip", type=int, default=20, help="Process every Nth frame to speed up")
    parser.add_argument("--model", default="yolov8s.pt")
    parser.add_argument("--video", default="airport_video.mp4")
    return parser.parse_args()


def main():
    args = parse_args()
    dp = DifferentialPrivacy(epsilon=args.epsilon)
    video_source = VideoSource(
        video_path=Path(args.video),
        model_path=args.model,
        threshold=args.threshold,
        frame_skip=args.frame_skip,
    )

    try:
        video_source.open()
        fps, total_frames = video_source.get_properties()

        print(f"Processing video: {total_frames} frames at {fps:.1f} FPS")
        print(f"Frame skip: {args.frame_skip}")
        print("-" * 60)
        print(f"{'Frame':<6} {'SysTime':<8} {'True':<5} {'DP':<5} {'Conf%':<6} {'Decision':<10}")
        print("-" * 60)

        processed_frames = 0
        for frame_count, frame in video_source.frames():
            processed_frames += 1
            true_count, avg_conf = video_source.count_people(frame)
            dp_count = dp.privatize_count(true_count)
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            decision = dp.classify(dp_count)

            print(
                f"{frame_count:<6} {timestamp:<8} {true_count:<5} {dp_count:<5} {avg_conf:<6.1f} {decision:<10}"
            )

    except (FileNotFoundError, RuntimeError) as error:
        print(f"Error: {error}")
        sys.exit(1)
    finally:
        video_source.close()

    print("-" * 60)
    print(f"Processed {processed_frames} frames out of {total_frames} total frames")
    print(f"Epsilon (DP): {args.epsilon}")


if __name__ == "__main__":
    main()
