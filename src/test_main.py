import unittest
from main import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_header(self):
        result = extract_title("# Hello")
        self.assertEqual(result, "Hello")

    def test_no_header(self):
        with self.assertRaises(Exception):
            extract_title("No h1 header here")

if __name__ == "__main__":
    unittest.main()