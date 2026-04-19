import random
import sys
import argparse
from pathlib import Path
import datetime

from dp import LaplaceDifferentialPrivacy, GaussianDifferentialPrivacy
from video_source import VideoSource

#File paths are relative to the script location
SCRIPT_DIR = Path(__file__).parent
# Global list of videos to process - edit this list to change videos
videos = ["airport_video.mp4", "test_video.mp4"]

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--threshold", type=float, default=0.30)
    parser.add_argument("--epsilon", type=float, default=0.7)
    parser.add_argument("--delta", type=float, default=1e-5)
    parser.add_argument("--noise_type", choices=['laplace', 'gaussian'], default=random.choice(['laplace', 'gaussian']))
    parser.add_argument("--frame_skip", type=int, default=20,)
    parser.add_argument("--model", default="yolov8s.pt")
    parser.add_argument("--video", nargs="+", default=videos)
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    if args.noise_type == 'gaussian':
        dp = GaussianDifferentialPrivacy(epsilon=args.epsilon, delta=args.delta)
    else:
        dp = LaplaceDifferentialPrivacy(epsilon=args.epsilon)

    for video in args.video:  # Loop over each video
        print(f"\n{'='*60}")
        print(f"Processing video/camera: {video}")
        print(f"{'='*60}")

        video_source = VideoSource(
            video_path= SCRIPT_DIR / video if not video.isdigit() and 'rtsp://' not in video else video,
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
            print(f"Error processing {video}: {error}")
            continue
        finally:
            video_source.close()

        print("-" * 60)
        print(f"Processed {processed_frames} frames out of {total_frames} total frames")
        print(f"Epsilon (DP): {args.epsilon}, Noise Type: {args.noise_type}")


if __name__ == "__main__":
    main()
