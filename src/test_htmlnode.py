import unittest

from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            tag="p",
            value="This is a paragraph text",
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        result = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), result)

    def test_repr(self):
        node = HTMLNode(
            tag="p",
            value="This is a paragraph text",
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )

        result = (
            "HTMLNode(p, This is a paragraph text, "
            "children: None, "
            "{'href': 'https://www.google.com', 'target': '_blank'})"
        )

        self.assertEqual(repr(node), result)

    def test_repr_empty_node(self):
        node = HTMLNode()
        self.assertEqual(
            repr(node),
            "HTMLNode(None, None, children: None, None)"
        )

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

    def test_leaf_to_html_with_props_ignored(self):
        node = LeafNode(
            "a",
            "Click here",
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )

        # props are ignored in your implementation
        self.assertEqual(
            node.to_html(),
            "<a>Click here</a>"
        )

    def test_leaf_no_value_raises(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>child</span></div>"
        )

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])

        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>"
        )

    def test_parent_to_html_no_tag_raises(self):
        node = ParentNode(None, [LeafNode("p", "text")])
        with self.assertRaises(ValueError) as context:
            node.to_html()

        self.assertEqual(
            str(context.exception),
            "invalid HTML: no tag"
        )

    def test_parent_to_html_no_children_raises(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError) as context:
            node.to_html()

        self.assertEqual(
            str(context.exception),
            "invalid HTML: no children"
        )

    def test_parent_to_html_mixed_children(self):
        node = ParentNode(
            "div",
            [
                LeafNode("p", "hello"),
                ParentNode("span", [LeafNode("b", "world")]),
            ],
        )

        self.assertEqual(
            node.to_html(),
            "<div><p>hello</p><span><b>world</b></span></div>"
        )

if __name__ == "__main__":
    unittest.main()