import unittest

from inline_markdown import *

class TestInlineMarkdown(unittest.TestCase):
    def test_split_delimiter_1(self):
        node1 = TextNode("This is text with a `code block` word", TextType.TEXT)
        node0 = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        node2 = split_nodes_delimiter([node1], "`", TextType.CODE)
        self.assertEqual(node0, node2)

    def test_split_delimiter_2(self):
        node1 = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
        node0 = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in the middle", TextType.TEXT),
        ]
        node2 = split_nodes_delimiter([node1], "**", TextType.BOLD)
        self.assertEqual(node0, node2)

    def test_extract_markdown_images_1(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_2(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

if __name__ == "__main__":
    unittest.main()