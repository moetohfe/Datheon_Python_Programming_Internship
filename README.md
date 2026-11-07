# Datheon Python Programming Internship

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)
![Tests](https://img.shields.io/badge/tests-15%20passing-brightgreen)
![Dependencies](https://img.shields.io/badge/dependencies-none-blue)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

Three Python projects built for the **Datheon Python Programming Internship (2026)**: a console game, a file automation tool, and a rule-based chatbot. Each one is written using only the Python standard library and comes with unit tests.

| | |
|---|---|
| **Intern** | Mohammad Tohfe |
| **Application ID** | DT-2026-HAVZJ |
| **Tasks completed** | Task 1 · Task 3 · Task 4 |

## Contents

- [Projects](#projects)
  - [Task 1 – Hangman Word Guessing Game](#task-1--hangman-word-guessing-game)
  - [Task 3 – Automated File Organizer](#task-3--automated-file-organizer--cleanup-utility)
  - [Task 4 – Rule-Based Chatbot](#task-4--rule-based-terminal-assistant--chatbot)
- [Getting Started](#getting-started)
- [Running the Tests](#running-the-tests)
- [Project Structure](#project-structure)
- [What I Learned](#what-i-learned)

## Projects

### Task 1 – Hangman Word Guessing Game

A terminal version of Hangman. The player guesses a hidden word one letter at a time and has 6 lives.

**Features**
- Random word chosen from `words.txt` with `random.choice()` (falls back to a built-in list if the file is missing)
- Masked word display, e.g. `P Y _ H _ N`
- ASCII gallows that update after every wrong guess
- Repeated guesses are detected and cost no lives
- Input validation (single letters only), victory/defeat screens, running score and "play again"

```bash
python task1_hangman/hangman.py
```

```
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========

Word:    L O O _
Missed:  X Z E
Lives left: 3
Guess a letter:
```

### Task 3 – Automated File Organizer & Cleanup Utility

A command-line tool that cleans up a cluttered folder (like Downloads) by sorting files into category subfolders based on their extension.

**Features**
- Scans the folder with `os.scandir()` and moves files with `shutil.move()`
- Categories: **Documents, Images, Videos, Audio, Archives, Code**, plus **Others** for anything unrecognized
- Handles name collisions safely by renaming (`report.pdf` → `report (1).pdf`), so nothing is ever overwritten
- Catches `PermissionError`, `FileExistsError` and other `OSError`s, logs them and keeps going
- Logs every action to the console and to `organizer.log`, then prints a summary table
- `--dry-run` mode previews the changes without moving anything
- Skips hidden files and subfolders

```bash
python task3_file_organizer/organizer.py ~/Downloads --dry-run   # preview first
python task3_file_organizer/organizer.py ~/Downloads             # then organize
```

```
========================================
 EXECUTION SUMMARY
========================================
 Archives         1 file(s)
 Code             1 file(s)
 Documents        2 file(s)
 Images           1 file(s)
 Videos           1 file(s)
----------------------------------------
 Relocated        6
 Skipped          0
========================================
```

### Task 4 – Rule-Based Terminal Assistant / Chatbot

**ShopBot**, a customer-support assistant for a small store. It understands questions about hours, location, shipping, returns, payment, products, prices and contact details.

**Features**
- Intents, regex patterns and replies are stored in `faq.json`, so the bot's knowledge can change without changing the code
- Input normalization: lowercase, whitespace cleanup, punctuation removal
- Regex keyword matching with pre-compiled patterns
- **Multi-intent recognition**: one message can ask several things and each is answered in order
- Conversation states: `GREETING → CHATTING → EXIT`
- Graceful fallback for unrecognized input and a `help` command
- Clean exit with `bye`, `exit`, `quit` or Ctrl+C

```bash
python task4_chatbot/chatbot.py
```

```
ShopBot: Hi! I'm ShopBot, your store assistant. Type 'help' to see what I can do.
You: hey, when are you open and can I return stuff?
ShopBot: We're open Monday-Friday 9am-6pm and Saturday 10am-4pm. We're closed on Sundays.
You can return any unused item within 30 days for a full refund. Just bring your receipt or order number.
You: bye
ShopBot: Thanks for chatting. Have a great day!
```

## Getting Started

**Requirements:** Python 3.8 or newer. There are no packages to install.

```bash
git clone https://github.com/moetohfe/Datheon_Python_Programming_Internship.git
cd Datheon_Python_Programming_Internship
python task1_hangman/hangman.py
```

## Running the Tests

The project has 15 unit tests written with Python's built-in `unittest` module.

```bash
python -m unittest discover -s tests -v
```

| Test file | What it checks |
|---|---|
| `test_hangman.py` | Word masking, gallows stages, word-list loading and fallback |
| `test_organizer.py` | Sorting into categories, collision renaming, hidden files, dry run |
| `test_chatbot.py` | Normalization, single and multi-intent matching, fallback, help |

## Project Structure

```
Datheon_Python_Programming_Internship/
├── task1_hangman/
│   ├── hangman.py          # Hangman game
│   └── words.txt           # Word list
├── task3_file_organizer/
│   └── organizer.py        # File organizer CLI
├── task4_chatbot/
│   ├── chatbot.py          # ShopBot assistant
│   └── faq.json            # Intents, patterns and responses
├── tests/
│   ├── test_hangman.py
│   ├── test_organizer.py
│   └── test_chatbot.py
├── .gitignore
├── LICENSE
└── README.md
```

## What I Learned

- **Clean program structure:** splitting each program into small, testable functions instead of one long script
- **Working with the filesystem safely:** `pathlib`, `os.scandir()`, `shutil`, handling errors without crashing, and never overwriting data
- **Text processing with regular expressions:** normalizing input and matching several patterns in one message
- **Data-driven design:** keeping the chatbot's content in JSON so it can grow without code changes
- **Testing:** writing unit tests with `unittest`, which caught a real whitespace bug in the chatbot's input normalization

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
