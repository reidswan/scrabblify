"""Tests the scrabblify.py script"""

import scrabblify
import unittest
import random
from dataclasses import dataclass

class TestScrabblify(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # ensure predictable results
        random.seed(987)

    def setUp(self):
        # ensure each test case starts with a fresh loaded_words
        scrabblify.loaded_words = {}

    def test_get_valid_args(self):
        @dataclass
        class TestCase:
            name: str
            args: list[str]
            expect_valid: bool
            expect_args: list[str]
            
        test_cases = [
            TestCase(
                name="no args provided",
                args=[],
                expect_valid=False,
                expect_args=[],
            ),
            TestCase(
                name="mixed case",
                args=["script_name", "abc", "XYZ", "SOMeThinGElse"],
                expect_valid=True,
                expect_args=["abc", "xyz", "somethingelse"],
            ),
            TestCase(
                name="invalid arg",
                args=["script_name", "abc", "XYZ", "i am not alpha", "ffgg"],
                expect_valid=False,
                expect_args=[],
            ),
        ]
        for case in test_cases:
            with self.subTest(case.name):
                res, valid = scrabblify.get_valid_args(case.args)
                self.assertEqual(case.expect_valid, valid)
                self.assertEqual(case.expect_args, res)

    def test_scrabblify_once(self):
        # ensure some words loaded
        for i in range(5):
            scrabblify.load_words_with_len(i + 1)
        
        scrabblify.loaded_words[7] = {'d': ['dragons']}
        
        @dataclass
        class TestCase:
            name: str
            word: str
            expect_word: str

        test_cases = [
            TestCase(name="0 length word", word="", expect_word=""),
            TestCase(name="no words have this length", word="geronimo", expect_word="geronimo"),
            TestCase(name="only our word has this length", word="dragons", expect_word="dragons"),
            TestCase(name="length 4", word="drag", expect_word="doom"),
            TestCase(name="length 2", word="of", expect_word="ow"),
            TestCase(name="length 3", word="hem", expect_word="hum"),
        ]
        for case in test_cases:
            with self.subTest(case.name):
                word = scrabblify.scrabblify_once(case.word)
                self.assertEqual(case.expect_word, word)

if __name__ == '__main__':
    unittest.main()
