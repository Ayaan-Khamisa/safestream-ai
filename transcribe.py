from faster_whisper import WhisperModel


def transcribe(audio_path):
	"""Return a list of words with start and end times (in seconds)."""
	model = WhisperModel("small", device="cpu", compute_type="int8")
	segments, info = model.transcribe(
		audio_path, language="en", word_timestamps=True
	)
	words = []
	for segment in segments:
		for w in segment.words:
			words.append({"word": w.word.strip(), "start": w.start, "end": w.end})
	return words


if __name__ == "__main__":
	for w in transcribe("test_audio.wav"):
		print(f'{w["start"]:6.2f} - {w["end"]:6.2f}  {w["word"]}')
