import json
import os.path
import sys
import logging
import random

# loaded_words is a cache of words already read from disk
# keyed first by the length of the words, then by first letter
# e.g. 
# {
#   ..., 
#   3: {
#       ...,
#       'g': [..., 'gem', 'gum', 'gun', 'god', ...], 
#       ...
#       },
#   ...,
# }
loaded_words = {} # type: dict[int, dict[str, list[str]]]

def help():
    """Shows a helpful message to the user indicating how to use this script"""

    print("Scrabblify usage")
    print("python3 scrabblify.py <words to scrabblify>")
    print()
    print("For example:")
    print("    $ python3 scrabblify.py he sings to the moon")
    print()
    print("Words may contain only the letters a through z, upper or lower case, separated by spaces")

def get_valid_args(args: list[str]) -> (list[str], bool):
    """get_args will check that the provided args are valid and return
    only those that the program should act on, stripping the script name.
    Returns: validated arg list, boolean indicating if the args were valid"""
    if len(args) < 2:
        return [], False
    
    result = []
    # args[1:] -> remove script name from argv
    for arg in args[1:]:
        if not arg.isalpha():
            return [], False
        result.append(arg.lower())

    return result, True

def load_words_with_len(len: int):
    """Loads words with the length `len` into the loaded_words dict"""

    if len in loaded_words:
        # words already loaded for this length
        return
    
    try:
        with open(os.path.join('data', f'words-{len}.json'), 'r') as infile:
            words_by_letter = json.load(infile)
            loaded_words[len] = words_by_letter
    except FileNotFoundError as e:
        # no words with length found; log but do not fail
        logging.debug(f"words with length {len} not found", e)

def scrabblify_once(word: str) -> str:
    """Finds a corresponding word with the same length and starting letter
    If one cannot be found, simply returns the given word"""
    
    if len(word) == 0:
        # sanity check
        return word
    elif len(word) not in loaded_words:
        # we have no words with the same length
        return word
    elif word[0] not in loaded_words[len(word)]:
        # we have no words starting with the first character of this word
        return word
    
    candidates = loaded_words[len(word)][word[0]]
    if len(candidates) == 0 or (len(candidates) == 1 and candidates[0] == word):
        # we either have no candidates, or our only candidate is the word we already have
        return word
    
    selected = random.choice(candidates)
    tries = 0
    while selected == word and tries < 5:
        # we could do this by cloning the list without `word`
        # or finding the index of `i` of `word` in `candidates` and then 
        # selecting a word from candidates[:i], candidates[i+1:] 
        # but that would be messy and this will work _most_ of the time, 
        # statistically speaking
        selected = random.choice(candidates)
        tries += 1

    return selected

def scrabblify(words: list[str]) -> list[str]:
    """Ensures the word lists are cached, then runs each word through the scrabblify_once function,
    returning the results"""
    result = []
    for word in words:
        load_words_with_len(len(word))
        result.append(scrabblify_once(word.lower()))
    return result

if __name__ == '__main__':
    args, valid = get_valid_args(sys.argv)
    if not valid:
        help()
        exit(2)
    
    print(" ".join(scrabblify(args)))
