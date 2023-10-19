# Scrabblify

Scrabblify is a [Python](https://www.python.org) script that can rejig your sentences, introducing you to a wealth of new, Scrabble-appropriate words! Given a sentence, Scrabblify will replace the words you give it with words of the same length, starting with the same first character.

For example, `happy wizard throws dynamite` might turn into `hardy whiner twists daughter`, or perhaps `hippy wisdom thumbs division`.

## Running Scrabblify

You will need to have an installation of [Python 3](https://www.python.org/downloads/). If you are running a modern version of macos, `python3` should already be installed. If not, a download along with detailed installation instructions are available [here](https://www.python.org/downloads/).

Then simply navigate to this directory in your terminal, and run the script with your candidate sentence:

```
$ cd /path/to/scrabblify
$ python3 scrabblify.py <your sentence>
```

where `<your sentence>` is replaced by the sentence you wish to rejig, for example

```
$ python3 scrabblify.py happy wizard throws dynamite
```

The words in `<your sentence>` may contain only the letters a through z, upper or lower case, and must be separated by spaces.

## Technical details

The words used in this script are sourced from [dwyl/english-words](https://github.com/dwyl/english-words).

They are bucketed into separate files by their length to minimize the number of files that need to be read on a given run of the script. Each file contains `JSON` which is keyed by the first letter of the words in the corresponding list. This bucketing is performed by the `data/ingest.py` script on the master `words.txt` file to produce `words-<i>.json`, where `<i>` is the length of the words in that file.

The scrabblify.py file can then only read words it might actually use based on the lengths of its inputs.

Unit tests are in the `test_scrabblify.py` file; run them either directly: `python3 test_scrabblify.py` or using the `unittest` module: `python3 -m unittest`
