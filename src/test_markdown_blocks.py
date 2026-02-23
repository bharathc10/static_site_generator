import unittest

from markdown_blocks import *
from textnode import *

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_heading_single_hash(self):
        block = "# Heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)


    def test_heading_six_hashes(self):
        block = "###### Small Heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)


    def test_not_heading_missing_space(self):
        block = "##Heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


    def test_code_block(self):
        block = "```\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)


    def test_not_code_block_missing_newline(self):
        block = "```print('hello')```"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


    def test_quote_block_single_line(self):
        block = "> This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)


    def test_quote_block_multi_line(self):
        block = "> First line\n> Second line"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)


    def test_unordered_list(self):
        block = "- item 1\n- item 2\n- item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)


    def test_ordered_list_valid(self):
        block = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)


    def test_ordered_list_wrong_start(self):
        block = "2. First\n3. Second"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


    def test_ordered_list_not_incrementing(self):
        block = "1. First\n3. Second"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


    def test_paragraph(self):
        block = "This is just a normal paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()