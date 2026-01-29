import unittest

from htmlnode import HTMLNode

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


if __name__ == "__main__":
    unittest.main()