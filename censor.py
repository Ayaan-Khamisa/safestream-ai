import argparse
import shutil
import subprocess
from pathlib import Path

from detect import clean, find_bad_words, load_bad_words
from extract_audio import extract_audio
from transcribe import transcribe

PADDING = 0.05  # seconds added either side, to cover small timing errors


def build_expression(segments):
    """Turn (start, end) pairs into an FFmpeg 'is this moment censored?' test."""
    parts = [
        f"between(t,{max(start - PADDING, 0):.3f},{end + PADDING:.3f})"
        for start, end in segments
    ]
    return "+".join(parts)


def censor_video(video_path, output_path, segments, mode="beep"):
    """Write a copy of the video with the given segments beeped or silenced."""
    if not segments:
        shutil.copy(video_path, output_path)
        return

    expr = build_expression(segments)

    if mode == "silence":
        graph = f"[0:a]volume=0:enable='{expr}'[aout]"
        inputs = ["-i", video_path]
    else:
        graph = (
            f"[0:a]volume=0:enable='{expr}'[muted];"
            f"[1:a]volume=0.3,volume=0:enable='not({expr})'[beep];"
            "[muted][beep]amix=inputs=2:duration=first:normalize=0[aout]"
        )
        inputs = ["-i", video_path, "-f", "lavfi", "-i", "sine=frequency=1000:sample_rate=48000"]

    command = [
        "ffmpeg", "-y", *inputs,
        "-filter_complex", graph,
        "-map", "0:v", "-map", "[aout]",
        "-c:v", "copy", "-c:a", "aac",
        output_path,
    ]
    subprocess.run(command, check=True)


def main():
    parser = argparse.ArgumentParser(
        description="Beep or silence bad words in a video's audio."
    )
    parser.add_argument("video", help="path to the input video, e.g. clip.mp4")
    parser.add_argument(
        "--mode",
        choices=["beep", "silence", "both"],
        default="both",
        help="what to replace bad words with (default: both)",
    )
    args = parser.parse_args()

    video = Path(args.video)
    if not video.exists():
        parser.error(f"file not found: {video}")

    audio_path = video.with_name(f"{video.stem}_audio.wav")
    extract_audio(str(video), str(audio_path))

    words = transcribe(str(audio_path))
    found = find_bad_words(words, load_bad_words())
    segments = [(w["start"], w["end"]) for w in found]
    for w in found:
        print("Censoring:", clean(w["word"]), f'{w["start"]:.2f}-{w["end"]:.2f}')
    print(f"{len(found)} word(s) flagged")

    modes = ["beep", "silence"] if args.mode == "both" else [args.mode]
    for mode in modes:
        output = video.with_name(f"{video.stem}_{mode}.mp4")
        censor_video(str(video), str(output), segments, mode=mode)
        print("Wrote", output)


if __name__ == "__main__":
    main()