"""Unit tests for Task 1 - Hangman."""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "task1_hangman"))
import hangman  # noqa: E402


class TestHangman(unittest.TestCase):
    def test_masked_word_hides_unguessed_letters(self):
        self.assertEqual(hangman.masked_word("loop", {"o"}), "_ O O _")

    def test_masked_word_fully_revealed(self):
        self.assertEqual(hangman.masked_word("cat", set("cat")), "C A T")

    def test_gallows_has_a_stage_per_mistake(self):
        self.assertEqual(len(hangman.GALLOWS), hangman.MAX_MISTAKES + 1)

    def test_load_words_skips_invalid_lines(self):
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
            f.write("Python\n\nhello world\n123\nloop\n")
        try:
            self.assertEqual(hangman.load_words(f.name), ["python", "loop"])
        finally:
            os.remove(f.name)

    def test_load_words_falls_back_when_file_missing(self):
        self.assertEqual(hangman.load_words("does_not_exist.txt"), hangman.DEFAULT_WORDS)


if __name__ == "__main__":
    unittest.main()
