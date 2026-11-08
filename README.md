## Demo

Watch the demo on LinkedIn: [SafeStream AI demo] https://github.com/user-attachments/assets/10d17a12-766b-4cd0-bc42-a0e55e3808e2

# SafeStream AI

Detects inappropriate language in a video's audio and replaces it with a beep or silence.

## How it works

1. **Extract audio** from the video with FFmpeg.
2. **Transcribe** it with faster-whisper, getting a start and end time for every word.
3. **Match** the transcript against a word list (`bad_words.txt`).
4. **Censor** the matched moments, writing one copy with beeps and one with silence. The video picture is copied unchanged.

## What I found when testing

I tested it on a 10-second clip of myself arguing about a video game. The smaller `base` speech model misheard "damn" as "done" and garbled another phrase. The larger `small` model transcribed the whole clip correctly, and all three swear words were beeped or silenced at the right moments. The project uses the `small` model.

## Setup (Windows)

1. Install Python 3.12, Git and FFmpeg. To install FFmpeg: `winget install --id Gyan.FFmpeg -e`
2. Create and activate a virtual environment:
   ```
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
   If PowerShell blocks the script, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once and try again.
3. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

The first run downloads the speech model, so it needs an internet connection and takes longer than later runs. The `av` library is pinned below version 19 because a newer version stopped working with faster-whisper when I tested.

## Usage

```
python censor.py yourvideo.mp4
```

This writes `yourvideo_beep.mp4` and `yourvideo_silence.mp4` next to the original. To make only one version:

```
python censor.py yourvideo.mp4 --mode beep
python censor.py yourvideo.mp4 --mode silence
```

Edit `bad_words.txt` (one lowercase word per line) to change what gets censored.

## Project structure

- `censor.py` is the main program, which you run from the command line.
- `extract_audio.py` pulls the audio out of the video.
- `transcribe.py` turns the audio into words with timestamps.
- `detect.py` matches the words against `bad_words.txt`.
- `bad_words.txt` is the list of words to censor.

## Limitations

- Speech recognition makes mistakes, so a swear word can be misheard and missed. Larger models help but are slower.
- It matches whole words from a list and knows nothing about context, so innocent uses of a listed word get flagged too.
- English only.
- Tested on `.mp4` files, and on one `.mov` re-wrap of the same clip. Other formats and codecs are untested.
I also ran a second test on a clip made with an AI text-to-speech voice. It was audio only, so I wrapped it in a plain black video with FFmpeg first. Every listed swear word in the script was beeped at the right moment. A clean synthetic voice is easier for speech recognition than a real person in a noisy room, so this shows the pipeline works on a different voice and file type. It doesn't show it will catch every word in real-world recordings.


I also ran a second test on a clip made with an AI text-to-speech voice. It was audio only, so I wrapped it in a plain black video with FFmpeg first. Every listed swear word in the script was beeped at the right moment. A clean synthetic voice is easier for speech recognition than a real person in a noisy room, so this shows the pipeline works on a different voice and file type. It doesn't show it will catch every word in real-world recordings.

