import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(tag = "p", value = "This is a paragraph text", 
                        props = {
                            "href": "https://www.google.com",
                            "target": "_blank",
                        })
        result = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), result)

    def test_repr(self):
        node = HTMLNode(
            tag="p",
            value="This is a paragraph text",
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )

        result = (
            "HTMLNode("
            "tag = 'p', "
            "value = 'This is a paragraph text', "
            "children = None, "
            "props = {'href': 'https://www.google.com', 'target': '_blank'}"
            ")"
        )

        self.assertEqual(repr(node), result)

    def test_repr_empty_node(self):
        node = HTMLNode()

        result = (
            "HTMLNode("
            "tag = None, "
            "value = None, "
            "children = None, "
            "props = None"
            ")"
        )

        self.assertEqual(repr(node), result)

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Heading")
        self.assertEqual(node.to_html(), "<h1>Heading</h1>")


    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Bold text")
        self.assertEqual(node.to_html(), "<b>Bold text</b>")
    
    def test_leaf_to_html_with_props(self):
        node = LeafNode(
            "a",
            "Click here",
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )

        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com" target="_blank">Click here</a>'
        )

if __name__ == "__main__":
    unittest.main()