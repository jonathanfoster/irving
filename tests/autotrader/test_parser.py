import os
from pathlib import Path
import unittest

from irving import autotrader


class ParserTestCase(unittest.TestCase):
    def test_parse_listings(self):
        file_dir = Path(__file__).parent
        listings1 = autotrader.parse_listings(
            os.path.join(file_dir, "search-results-1.html")
        )
        listings2 = autotrader.parse_listings(
            os.path.join(file_dir, "search-results-2.html")
        )
        self.assertEqual(len(listings1 + listings2), 132)
