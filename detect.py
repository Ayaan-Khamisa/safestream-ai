import re
from transcribe import transcribe


def load_bad_words(path="bad_words.txt"):
    """Read the word list into a set, ignoring blank lines."""
    with open(path, encoding="utf-8") as f:
        return {line.strip().lower() for line in f if line.strip()}


def clean(word):
    """Lowercase a word and strip punctuation, so 'Crap,' becomes 'crap'."""
    return re.sub(r"[^a-z0-9']", "", word.lower())


def find_bad_words(words, bad_words):
    """Return only the transcript words that are on the bad-words list."""
    return [w for w in words if clean(w["word"]) in bad_words]


if __name__ == "__main__":
    bad_words = load_bad_words()
    found = find_bad_words(transcribe("test_audio.wav"), bad_words)
    for w in found:
        print(f'{w["start"]:6.2f} - {w["end"]:6.2f}  {clean(w["word"])}')
    print(f"{len(found)} word(s) flagged")