# SafeStream AI

Detects inappropriate language in a video's audio and replaces it with a beep or silence.

## How it works

1. **Extract audio** from the video with FFmpeg.
2. **Transcribe** it with faster-whisper, getting a start and end time for every word.
3. **Match** the transcript against a word list (`bad_words.txt`).
4. **Censor** the matched moments, writing one copy with beeps and one with silence. The video picture is copied unchanged.

## What I found when testing

I tested it on a 10-second clip of myself arguing about a video game. The smaller `base` speech model misheard "damn" as "done" and garbled another phrase. The larger `small` model transcribed the whole clip correctly, and all three swear words were beeped or silenced at the right moments.

## Setup (Windows)

1. Install Python 3.12, Git and FFmpeg. FFmpeg: `winget install --id Gyan.FFmpeg -e`
2. Create and activate a virtual environment:
   ```
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
3. Install dependencies: `pip install -r requirements.txt`

## Usage

## Usage

```
python censor.py yourvideo.mp4
```

This writes `yourvideo_beep.mp4` and `yourvideo_silence.mp4` next to the original. To make only one version:

```
python censor.py yourvideo.mp4 --mode beep
python censor.py yourvideo.mp4 --mode silence
```

Edit `bad_words.txt` (one lowercase word per line) to change what gets censored.## Limitations

- Speech recognition makes mistakes, so a swear word can be misheard and missed. Larger models help but are slower.
- It matches whole words from a list and knows nothing about context, so innocent uses of a listed word get flagged too.
- English only.