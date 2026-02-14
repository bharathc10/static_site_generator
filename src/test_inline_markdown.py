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

class TestSplitImages(unittest.TestCase):

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_single_image(self):
        node = TextNode("Hello ![alt](url.png)", TextType.TEXT)

        self.assertListEqual(
            [
                TextNode("Hello ", TextType.TEXT),
                TextNode("alt", TextType.IMAGE, "url.png"),
            ],
            split_nodes_image([node]),
        )

    def test_image_at_start(self):
        node = TextNode("![alt](url.png) end", TextType.TEXT)

        self.assertListEqual(
            [
                TextNode("alt", TextType.IMAGE, "url.png"),
                TextNode(" end", TextType.TEXT),
            ],
            split_nodes_image([node]),
        )

    def test_image_at_end(self):
        node = TextNode("start ![alt](url.png)", TextType.TEXT)

        self.assertListEqual(
            [
                TextNode("start ", TextType.TEXT),
                TextNode("alt", TextType.IMAGE, "url.png"),
            ],
            split_nodes_image([node]),
        )

    def test_adjacent_images(self):
        node = TextNode("![a](1.png)![b](2.png)", TextType.TEXT)

        self.assertListEqual(
            [
                TextNode("a", TextType.IMAGE, "1.png"),
                TextNode("b", TextType.IMAGE, "2.png"),
            ],
            split_nodes_image([node]),
        )

    def test_no_images(self):
        node = TextNode("just plain text", TextType.TEXT)
        self.assertListEqual([node], split_nodes_image([node]))

    def test_non_text_node(self):
        node = TextNode("image", TextType.IMAGE, "url.png")
        self.assertListEqual([node], split_nodes_image([node]))

    def test_multiple_nodes_input(self):
        nodes = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("![alt](url.png)", TextType.TEXT),
            TextNode(" world", TextType.TEXT),
        ]

        self.assertListEqual(
            [
                TextNode("Hello ", TextType.TEXT),
                TextNode("alt", TextType.IMAGE, "url.png"),
                TextNode(" world", TextType.TEXT),
            ],
            split_nodes_image(nodes),
        )

    def test_empty_alt_text(self):
        node = TextNode("![](img.png)", TextType.TEXT)

        self.assertListEqual(
            [
                TextNode("", TextType.IMAGE, "img.png"),
            ],
            split_nodes_image([node]),
        )

class TestSplitLinks(unittest.TestCase):

    def test_multiple_links(self):
        node = TextNode(
            "Visit [Google](https://google.com) and [YouTube](https://youtube.com)",
            TextType.TEXT,
        )

        self.assertListEqual(
            [
                TextNode("Visit ", TextType.TEXT),
                TextNode("Google", TextType.LINK, "https://google.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("YouTube", TextType.LINK, "https://youtube.com"),
            ],
            split_nodes_link([node]),
        )

    def test_single_link(self):
        node = TextNode("Go to [site](url.com)", TextType.TEXT)

        self.assertListEqual(
            [
                TextNode("Go to ", TextType.TEXT),
                TextNode("site", TextType.LINK, "url.com"),
            ],
            split_nodes_link([node]),
        )

    def test_link_at_start(self):
        node = TextNode("[site](url.com) end", TextType.TEXT)

        self.assertListEqual(
            [
                TextNode("site", TextType.LINK, "url.com"),
                TextNode(" end", TextType.TEXT),
            ],
            split_nodes_link([node]),
        )

    def test_link_at_end(self):
        node = TextNode("start [site](url.com)", TextType.TEXT)

        self.assertListEqual(
            [
                TextNode("start ", TextType.TEXT),
                TextNode("site", TextType.LINK, "url.com"),
            ],
            split_nodes_link([node]),
        )

    def test_adjacent_links(self):
        node = TextNode("[a](1)[b](2)", TextType.TEXT)

        self.assertListEqual(
            [
                TextNode("a", TextType.LINK, "1"),
                TextNode("b", TextType.LINK, "2"),
            ],
            split_nodes_link([node]),
        )

    def test_no_links(self):
        node = TextNode("plain text", TextType.TEXT)
        self.assertListEqual([node], split_nodes_link([node]))

    def test_non_text_node(self):
        node = TextNode("Google", TextType.LINK, "url")
        self.assertListEqual([node], split_nodes_link([node]))

    def test_image_not_split_as_link(self):
        node = TextNode("![alt](img.png)", TextType.TEXT)
        self.assertListEqual([node], split_nodes_link([node]))

    def test_multiple_nodes_input(self):
        nodes = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("[site](url.com)", TextType.TEXT),
            TextNode(" world", TextType.TEXT),
        ]

        self.assertListEqual(
            [
                TextNode("Hello ", TextType.TEXT),
                TextNode("site", TextType.LINK, "url.com"),
                TextNode(" world", TextType.TEXT),
            ],
            split_nodes_link(nodes),
        )

class TestTextToTextnodes(unittest.TestCase):
    def test_example_output(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        result = text_to_textnodes(text)
        self.assertEqual(expected, result)  # Verified True[code:1]

    def test_mixed_delimiters_multiple(self):
        text = "Test **bold** _italic_ `code` and **nested** styles"
        result = text_to_textnodes(text)
        expected = [
            TextNode("Test ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("nested", TextType.BOLD),
            TextNode(" styles", TextType.TEXT),
        ]
        self.assertEqual(expected, result)

    def test_links_and_images_together(self):
        text = "See [link](https://ex.com) and ![img](img.png) [another](https://ex2.com)"
        expected = [
            TextNode("See ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://ex.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "img.png"),
            TextNode(" ", TextType.TEXT),
            TextNode("another", TextType.LINK, "https://ex2.com"),
        ]
        self.assertEqual(expected, text_to_textnodes(text))

    def test_unclosed_delimiter_raises(self):
        with self.assertRaises(Exception):
            text_to_textnodes("Unclosed **bold")

    def test_empty_string(self):
        self.assertEqual([], text_to_textnodes(""))

    def test_plain_text(self):
        text = "No markdown here"
        self.assertEqual([TextNode(text, TextType.TEXT)], text_to_textnodes(text))

    def test_adjacent_elements(self):
        text = "**b**_i_`c`![i1](u1)![i2](u2)[l1](v1)[l2](v2)"
        expected = [
            TextNode("b", TextType.BOLD),
            TextNode("i", TextType.ITALIC),
            TextNode("c", TextType.CODE),
            TextNode("i1", TextType.IMAGE, "u1"),
            TextNode("i2", TextType.IMAGE, "u2"),
            TextNode("l1", TextType.LINK, "v1"),
            TextNode("l2", TextType.LINK, "v2"),
        ]
        self.assertEqual(expected, text_to_textnodes(text))

    def test_code_before_bold(self):
        text = "`code` **bold**"
        # Your order (code first) correctly splits both
        expected = [
            TextNode("code", TextType.CODE),
            TextNode(" ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ]
        self.assertEqual(expected, text_to_textnodes(text))

if __name__ == "__main__":
    unittest.main()

    