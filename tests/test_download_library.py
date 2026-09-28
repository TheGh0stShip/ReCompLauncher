import os
import unittest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt6.QtWidgets import QApplication, QLabel, QWidget

import recomplauncher as launcher


class _Parent(QWidget):
    def __init__(self):
        super().__init__()
        self.games = []
        self._threads = []


class DownloadLibraryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.parent = _Parent()
        self.dialog = launcher.DownloadLibraryDialog(self.parent)

    def tearDown(self):
        self.dialog.close()
        self.parent.close()

    def test_catalog_has_one_row_per_official_repository(self):
        repos = [entry["github_repo"].lower() for entry in self.dialog.entries]
        self.assertTrue(repos)
        self.assertEqual(len(repos), len(set(repos)))
        self.assertEqual(self.dialog.list.count(), len(repos))

    def test_epoch_and_equinox_is_downloadable(self):
        epoch = next(entry for entry in self.dialog.entries
                     if entry["github_repo"] == "ZakyPew/epoch-equinox")
        self.assertEqual(
            epoch["title"],
            "The Legend of Zelda: Oracle of Ages & Oracle of Seasons")

    def test_dialog_explicitly_excludes_roms(self):
        text = " ".join(label.text() for label in self.dialog.findChildren(QLabel))
        self.assertIn("No ROMs or original game data", text)

    def test_existing_game_is_marked_as_in_library(self):
        self.parent.games = [{"github_repo": "ZakyPew/epoch-equinox"}]
        self.dialog._fill()
        matches = [self.dialog.list.item(i).text()
                   for i in range(self.dialog.list.count())
                   if "Oracle of Ages" in self.dialog.list.item(i).text()]
        self.assertEqual(len(matches), 1)
        self.assertTrue(matches[0].startswith("✓"))


if __name__ == "__main__":
    unittest.main()
