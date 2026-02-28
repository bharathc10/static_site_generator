import unittest
from gencontent import *

class TestExtractTitle(unittest.TestCase):

    # 1. Success Case: Standard H1
    def test_basic_h1(self):
        md = "# Hello World"
        self.assertEqual(extract_title(md), "Hello World")

    # 2. Success Case: H1 with surrounding whitespace
    def test_h1_with_whitespace(self):
        md = "#    Spacing Test    "
        self.assertEqual(extract_title(md), "Spacing Test")

    # 3. Success Case: H1 not on the first line
    def test_h1_not_first_line(self):
        md = "\n\n# Found Me"
        self.assertEqual(extract_title(md), "Found Me")

    # 4. Error Case: No H1 at all
    def test_no_h1(self):
        md = "## Just an H2\nPlain text here."
        with self.assertRaisesRegex(Exception, "No h1 heading"):
            extract_title(md)

    # 5. Edge Case: Missing the space (Invalid Markdown H1)
    def test_h1_no_space(self):
        # Markdown requires a space after the '#' to be an H1
        md = "#NoSpace"
        with self.assertRaises(Exception):
            extract_title(md)

    # 6. Edge Case: Multiple H1s (Should return the first one)
    def test_multiple_h1s(self):
        md = "# First\n# Second"
        self.assertEqual(extract_title(md), "First")

if __name__ == '__main__':
    unittest.main()