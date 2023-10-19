import os.path
from collections import defaultdict
import json

def load_words(path: str) -> list[str]:
    with open(path) as infile:
        return infile.readlines()

def dump_words(path: str, words: dict[str, str]):
    with open(path, 'w') as outfile:
        json.dump(words, outfile)

if __name__ == '__main__':
    words = load_words(os.path.join("data", "words.txt"))
    
    words_by_len = defaultdict(lambda: defaultdict(list))
    for word in words:
        word = word.strip().lower()
        if len(word) == 0:
            continue

        words_by_len[len(word)][word[0]].append(word.lower())

    for wlen, words in words_by_len.items():
        dump_words(os.path.join("data", f"words-{wlen}.json"), words)
