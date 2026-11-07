"""Unit tests for Task 4 - Chatbot."""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "task4_chatbot"))
import chatbot  # noqa: E402


class TestChatbot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = chatbot.load_intents()

    def intents_for(self, text):
        return [i["name"] for i in chatbot.match_intents(chatbot.normalize(text), self.data["intents"])]

    def test_normalize(self):
        self.assertEqual(chatbot.normalize("  Hello,   THERE!! "), "hello there")

    def test_single_intent(self):
        self.assertEqual(self.intents_for("What time do you open?"), ["hours"])

    def test_multi_intent_in_order(self):
        self.assertEqual(self.intents_for("Do you ship, and what's your return policy?"),
                         ["shipping", "returns"])

    def test_greeting_dropped_when_question_asked(self):
        reply = chatbot.respond("hi, where are you located?", self.data)
        self.assertIn("Main Street", reply)
        self.assertNotIn("Hello", reply)

    def test_fallback_for_unknown_input(self):
        self.assertIn(chatbot.respond("asdfgh qwerty", self.data), self.data["fallback"])

    def test_help_lists_topics(self):
        self.assertIn("shipping", chatbot.respond("help", self.data))


if __name__ == "__main__":
    unittest.main()
