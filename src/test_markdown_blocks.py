import unittest

from markdown_blocks import *
from textnode import *
from htmlnode import *

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
    
    def test_paragraphs_markdown(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock_markdown(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    
    def test_unordered_list_markdown(self):
        md = """
- This is a **bold** item
- This is a normal item
- This has _italic_ text
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a <b>bold</b> item</li><li>This is a normal item</li><li>This has <i>italic</i> text</li></ul></div>",
        )

    def test_ordered_list_markdown(self):
        md = """
1. First item with `code`
2. Second item
3. Third item with **bold**
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item with <code>code</code></li><li>Second item</li><li>Third item with <b>bold</b></li></ol></div>",
        )

if __name__ == "__main__":
    unittest.main()