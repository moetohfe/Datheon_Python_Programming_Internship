"""Unit tests for Task 3 - File Organizer."""

import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "task3_file_organizer"))
import organizer  # noqa: E402


class TestOrganizer(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.folder = Path(self.tmp.name)
        for name in ["report.pdf", "photo.JPG", "clip.mp4", "backup.zip",
                     "script.py", "notes.unknown", ".hidden"]:
            (self.folder / name).touch()

    def tearDown(self):
        self.tmp.cleanup()

    def test_files_move_into_category_folders(self):
        stats = organizer.organize(self.folder)
        self.assertTrue((self.folder / "Documents" / "report.pdf").exists())
        self.assertTrue((self.folder / "Images" / "photo.JPG").exists())
        self.assertTrue((self.folder / "Videos" / "clip.mp4").exists())
        self.assertTrue((self.folder / "Archives" / "backup.zip").exists())
        self.assertTrue((self.folder / "Code" / "script.py").exists())
        self.assertTrue((self.folder / "Others" / "notes.unknown").exists())
        self.assertEqual(sum(stats.values()), 6)

    def test_hidden_files_are_left_alone(self):
        organizer.organize(self.folder)
        self.assertTrue((self.folder / ".hidden").exists())

    def test_name_collision_is_renamed(self):
        (self.folder / "Documents").mkdir()
        (self.folder / "Documents" / "report.pdf").touch()
        organizer.organize(self.folder)
        self.assertTrue((self.folder / "Documents" / "report (1).pdf").exists())

    def test_dry_run_moves_nothing(self):
        organizer.organize(self.folder, dry_run=True)
        self.assertTrue((self.folder / "report.pdf").exists())
        self.assertFalse((self.folder / "Documents").exists())


if __name__ == "__main__":
    unittest.main()
