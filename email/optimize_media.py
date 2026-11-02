"""Rebuild the full-length web demos: python -m pip install imageio-ffmpeg."""

import argparse
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import imageio_ffmpeg


ROOT = Path(__file__).resolve().parents[1]
DESTINATION = ROOT / "email/assets/video/web"
# Historical source names do not always match the action in the recording.
# The arm source is local presentation material; keep a copy to rebuild it.
CLIPS = [
    ("apple-grasp", "static/videos/ACT筷子.mp4", "960:540", 28),
    ("bottle-grasp", "static/videos/瓶子抓取.mp4", "960:540", 28),
    ("inhand-rotation", "static/videos/carousel1.mp4", "960:540", 28),
    ("gesture-following", "static/videos/follow_final.mp4", "1080:720", 29),
    ("arm-teleoperation", "program/static/videos/piper_arm.mp4", "800:640", 27),
    # Reuse the compact EEG export without another lossy encode.
    ("eeg-control", "email/assets/video/eeg-control.mp4", None, None),
    ("chopsticks", "static/videos/水果抓取.mp4", "406:720", 29),
]


def encode(clip):
    name, source, dimensions, crf = clip
    destination = DESTINATION / f"{name}.mp4"
    if arguments.force or not destination.exists():
        temporary = destination.with_suffix(".partial.mp4")
        command = [
            imageio_ffmpeg.get_ffmpeg_exe(), "-hide_banner", "-loglevel", "error", "-y",
            "-i", str(ROOT / source), "-map", "0:v:0", "-an", "-sn", "-dn",
        ]
        command += [
            "-vf", f"scale={dimensions}:flags=lanczos", "-r", "30",
            "-c:v", "libx264", "-preset", "slow", "-crf", str(crf),
            "-maxrate", "1400k", "-bufsize", "1400k", "-g", "60", "-keyint_min", "30",
            "-pix_fmt", "yuv420p", "-profile:v", "high", "-level:v", "3.1",
            "-threads", "4",
        ] if dimensions else ["-c:v", "copy"]
        command += [
            "-map_metadata", "-1", "-movflags", "+faststart",
            str(temporary),
        ]
        subprocess.run(command, check=True)
        temporary.replace(destination)
    return {"file": destination.name, "bytes": destination.stat().st_size, "dimensions": dimensions, "crf": crf}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="Rebuild existing web videos")
    parser.add_argument("--clip", action="append", choices=[clip[0] for clip in CLIPS], help="Build only selected clips")
    arguments = parser.parse_args()
    DESTINATION.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=2) as executor:
        clips = [clip for clip in CLIPS if not arguments.clip or clip[0] in arguments.clip]
        for result in executor.map(encode, clips):
            print(json.dumps(result), flush=True)
