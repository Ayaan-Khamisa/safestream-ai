import subprocess


def extract_audio(video_path, audio_path):
    """Pull the audio out of a video as a mono 16 kHz WAV file."""
    command = [
        "ffmpeg",
        "-y",             # overwrite the output file if it already exists
        "-i", video_path,  # the input video
        "-vn",            # ignore the video, keep only audio
        "-ac", "1",       # mono
        "-ar", "16000",   # 16,000 samples per second (what speech models expect)
        audio_path,
    ]
    subprocess.run(command, check=True)


if __name__ == "__main__":
    extract_audio("test.mp4", "test_audio.wav")
    print("Audio saved to test_audio.wav")
    