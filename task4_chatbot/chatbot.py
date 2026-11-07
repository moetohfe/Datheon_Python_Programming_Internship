"""
Rule-Based Interactive Terminal Assistant / Chatbot
Task 4 - Datheon Python Programming Internship

A customer-support bot for a small store. It loads intents from faq.json,
matches user input with regular expressions, can answer several intents
in one message, and falls back gracefully when it doesn't understand.

Conversation states: GREETING -> CHATTING -> EXIT
Type 'bye', 'exit' or 'quit' to leave, or 'help' for a list of topics.
"""

import json
import os
import random
import re

FAQ_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "faq.json")
EXIT_WORDS = {"bye", "exit", "quit", "goodbye"}


def load_intents(path=FAQ_FILE):
    """Load the bot name, intents and fallback replies from JSON."""
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as err:
        raise SystemExit(f"Could not load {path}: {err}")

    # Pre-compile each intent's regex patterns once for speed
    for intent in data["intents"]:
        intent["compiled"] = [re.compile(p, re.IGNORECASE) for p in intent["patterns"]]
    return data


def normalize(text):
    """Lowercase, trim, and remove punctuation except apostrophes."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s']", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def match_intents(text, intents):
    """Return every intent whose patterns appear in the text, in order of appearance."""
    hits = []
    for intent in intents:
        for pattern in intent["compiled"]:
            m = pattern.search(text)
            if m:
                hits.append((m.start(), intent))
                break
    hits.sort(key=lambda h: h[0])
    return [intent for _, intent in hits]


def respond(user_text, data):
    """Build the bot's reply for one user message."""
    text = normalize(user_text)
    if not text:
        return "Please type something - I'm listening!"
    if text == "help":
        topics = ", ".join(i["name"] for i in data["intents"] if i["name"] not in ("greeting", "thanks"))
        return f"I can help with: {topics}. Type 'bye' to exit."

    intents = match_intents(text, data["intents"])
    # Low confidence: nothing matched
    if not intents:
        return random.choice(data["fallback"])

    # If the user greeted AND asked something, skip the greeting reply
    if len(intents) > 1:
        intents = [i for i in intents if i["name"] != "greeting"]
    return "\n".join(random.choice(i["responses"]) for i in intents)


def main():
    data = load_intents()
    name = data.get("bot_name", "Bot")
    state = "GREETING"

    while state != "EXIT":
        if state == "GREETING":
            print(f"{name}: Hi! I'm {name}, your store assistant. Type 'help' to see what I can do.")
            state = "CHATTING"
            continue

        try:
            user = input("You: ")
        except (EOFError, KeyboardInterrupt):
            user = "bye"
            print()

        if normalize(user) in EXIT_WORDS:
            print(f"{name}: Thanks for chatting. Have a great day!")
            state = "EXIT"
        else:
            print(f"{name}: {respond(user, data)}")


if __name__ == "__main__":
    main()
