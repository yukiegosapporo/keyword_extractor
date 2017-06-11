import unittest
import colorlog

from functions import get_module_path, KeyphraseExtractor
from config import logger

logger.setLevel(colorlog.colorlog.logging.INFO)

class TestKeywordExtractor(unittest.TestCase):
    def setUp(self):
        self.project_path = get_module_path(__file__)
        self.KE1 = KeyphraseExtractor(
            self.project_path,
            True,
            23)
        self.KE2 = KeyphraseExtractor(
            self.project_path,
            False,
            12)

    def test_with_use_cluster(self):
        self.KE1.get_phrase_list()
        self.assertGreaterEqual(len(self.KE1.phrase_list), 0)
        self.KE1.get_phrase_scores()
        self.assertGreaterEqual(len(self.KE1.phrase_scores), 0)
        self.KE1.get_key_phrases()
        self.assertEqual(len(self.KE1.key_phrases), 23)

    def test_without_use_cluster(self):
        self.KE2.get_phrase_list()
        self.assertGreaterEqual(len(self.KE2.phrase_list), 0)
        self.KE2.get_phrase_scores()
        self.assertGreaterEqual(len(self.KE2.phrase_scores), 0)
        self.KE2.get_key_phrases()
        self.assertEqual(len(self.KE2.key_phrases), 12)


if __name__ == '__main__':
    unittest.main()