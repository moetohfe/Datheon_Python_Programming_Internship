"""
Hangman Word Guessing Game (Console)
Task 1 - Datheon Python Programming Internship

The player guesses a hidden word one letter at a time.
They lose after 6 wrong guesses. Repeated guesses are not penalised.
"""

import os
import random

MAX_MISTAKES = 6
WORDS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "words.txt")

# Fallback list, used only if words.txt is missing or empty
DEFAULT_WORDS = ["python", "variable", "function", "keyboard", "internship",
                 "algorithm", "terminal", "dictionary", "loop", "string"]

# ASCII gallows, one stage per number of mistakes (0-6)
GALLOWS = [
    """
  +---+
  |   |
      |
      |
      |
      |
=========""",
    """
  +---+
  |   |
  O   |
      |
      |
      |
=========""",
    """
  +---+
  |   |
  O   |
  |   |
      |
      |
=========""",
    """
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========""",
    """
  +---+
  |   |
  O   |
 /|\\  |
      |
      |
=========""",
    """
  +---+
  |   |
  O   |
 /|\\  |
 /    |
      |
=========""",
    """
  +---+
  |   |
  O   |
 /|\\  |
 / \\  |
      |
=========""",
]


def load_words(path=WORDS_FILE):
    """Read alphabetic words from a text file, one per line."""
    try:
        with open(path, encoding="utf-8") as f:
            words = [w.strip().lower() for w in f if w.strip().isalpha()]
        return words or DEFAULT_WORDS
    except FileNotFoundError:
        return DEFAULT_WORDS


def masked_word(word, guessed):
    """Return the word with unguessed letters shown as underscores."""
    return " ".join(ch.upper() if ch in guessed else "_" for ch in word)


def get_guess(already_guessed):
    """Ask until the player enters a single new letter."""
    while True:
        guess = input("Guess a letter: ").strip().lower()
        if len(guess) != 1 or not guess.isalpha():
            print("Please enter exactly one letter (a-z).")
        elif guess in already_guessed:
            print(f"You already guessed '{guess.upper()}'. Try another letter (no penalty).")
        else:
            return guess


def play_round(word):
    """Play one game. Returns True if the player wins."""
    correct, wrong = set(), set()

    while len(wrong) < MAX_MISTAKES:
        print(GALLOWS[len(wrong)])
        print("\nWord:   ", masked_word(word, correct))
        print("Missed: ", " ".join(sorted(l.upper() for l in wrong)) or "-")
        print(f"Lives left: {MAX_MISTAKES - len(wrong)}")

        guess = get_guess(correct | wrong)
        if guess in word:
            correct.add(guess)
            print(f"Nice! '{guess.upper()}' is in the word.")
            if set(word) <= correct:
                print("\n" + "=" * 34)
                print(f"  YOU WIN! The word was {word.upper()}")
                print("=" * 34)
                return True
        else:
            wrong.add(guess)
            print(f"Sorry, '{guess.upper()}' is not in the word.")

    print(GALLOWS[-1])
    print("\n" + "=" * 34)
    print(f"  GAME OVER! The word was {word.upper()}")
    print("=" * 34)
    return False


def main():
    words = load_words()
    wins = losses = 0
    print("Welcome to HANGMAN!")
    while True:
        if play_round(random.choice(words)):
            wins += 1
        else:
            losses += 1
        print(f"Score -> Wins: {wins}  Losses: {losses}")
        if input("\nPlay again? (y/n): ").strip().lower() != "y":
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()
