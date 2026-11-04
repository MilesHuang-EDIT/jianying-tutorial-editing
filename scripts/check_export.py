#!/usr/bin/env python3
"""Read-only checks for the final tutorial video. Requires FFmpeg and FFprobe."""

import argparse
import json
import math
import re
import subprocess
import sys
from fractions import Fraction
from pathlib import Path


def positive_fraction(value):
    try:
        number = Fraction(value)
    except (ValueError, ZeroDivisionError) as error:
        raise argparse.ArgumentTypeError("expected a positive number") from error
    if number <= 0:
        raise argparse.ArgumentTypeError("expected a positive number")
    return number


def run(command):
    result = subprocess.run(command, capture_output=True, text=True, errors="replace")
    if result.returncode:
        detail = result.stderr.strip() or f"exit {result.returncode}"
        raise RuntimeError(f"{command[0]} failed: {detail[-2000:]}")
    return result


def inspect(args):
    source = str(args.video.resolve(strict=True))
    probe = run([
        args.ffprobe, "-v", "error", "-show_streams", "-show_format", "-of", "json", source,
    ])
    media = json.loads(probe.stdout)
    streams = media["streams"]
    video = next((
        stream for stream in streams
        if stream["codec_type"] == "video"
        and not stream.get("disposition", {}).get("attached_pic")
    ), None)
    if video is None:
        raise ValueError("no video stream")

    audio = [stream for stream in streams if stream["codec_type"] == "audio"]
    width, height = video["width"], video["height"]
    rotation = next((
        item["rotation"] for item in video.get("side_data_list", []) if "rotation" in item
    ), 0)
    if round(rotation) % 180 == 90:
        width, height = height, width
    size = f"{width}x{height}"
    fps = video.get("avg_frame_rate", "0/0")
    duration = float(media["format"]["duration"])
    if not math.isfinite(duration) or duration <= 0:
        raise ValueError("invalid container duration")

    issues = []
    if args.size and size != args.size:
        issues.append(f"expected {args.size}, got {size}")
    if args.fps and (fps == "0/0" or Fraction(fps) != args.fps):
        issues.append(f"expected average FPS {args.fps}, got {fps}")
    if args.max_seconds is not None and duration > args.max_seconds:
        issues.append(f"duration exceeds {float(args.max_seconds):g} seconds")
    if args.audio == "present" and not audio:
        issues.append("expected an audio stream")
    if args.audio == "absent" and audio:
        issues.append("expected no audio stream")

    report = {
        "file": source,
        "size": size,
        "average_fps": fps,
        "duration_seconds": duration,
        "video_codec": video.get("codec_name"),
        "audio_streams": [{
            "codec": stream.get("codec_name"),
            "sample_rate": stream.get("sample_rate"),
            "channels": stream.get("channels"),
        } for stream in audio],
        "issues": issues,
    }

    try:
        run([
            args.ffmpeg, "-nostdin", "-v", "error", "-xerror", "-i", source,
            "-map", "0:V", "-map", "0:a?", "-f", "null", "-",
        ])
        report["full_decode"] = "passed"
    except (OSError, RuntimeError) as error:
        report["full_decode"] = "failed"
        issues.append(str(error))

    if args.loudness:
        if audio:
            try:
                report["first_audio_loudness"] = measure_loudness(args.ffmpeg, source)
            except (OSError, RuntimeError, ValueError) as error:
                issues.append(str(error))
        else:
            issues.append("loudness requested but there is no audio stream")
    return report


def measure_loudness(ffmpeg, source):
    scan = run([
        ffmpeg, "-nostdin", "-hide_banner", "-nostats", "-v", "info", "-xerror",
        "-i", source, "-map", "0:a:0", "-af", "loudnorm=print_format=json",
        "-f", "null", "-",
    ])
    match = re.search(r'\{\s*"input_i"\s*:.*?\}', scan.stderr, re.DOTALL)
    if match is None:
        raise ValueError("FFmpeg did not report loudness")
    data = json.loads(match.group())
    return {"integrated_lufs": data["input_i"], "true_peak_dbtp": data["input_tp"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", type=Path)
    parser.add_argument("--size", help="expected display size, such as 1920x1080")
    parser.add_argument("--fps", type=positive_fraction, help="expected average FPS, such as 30000/1001")
    parser.add_argument("--max-seconds", type=positive_fraction)
    parser.add_argument("--audio", choices=("present", "absent"))
    parser.add_argument("--loudness", action="store_true")
    parser.add_argument("--ffmpeg", default="ffmpeg")
    parser.add_argument("--ffprobe", default="ffprobe")
    args = parser.parse_args()
    try:
        report = inspect(args)
    except (OSError, RuntimeError, ValueError, KeyError, ZeroDivisionError) as error:
        print(str(error), file=sys.stderr)
        return 1
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if report["issues"] else 0


if __name__ == "__main__":
    sys.exit(main())
