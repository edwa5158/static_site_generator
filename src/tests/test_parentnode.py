import unittest

from html_leafnode import LeafNode
from html_parentnode import ParentNode
from html_void_node import VoidNode
from tests.utils import expected_error


class TestParentNode(unittest.TestCase):

    def test_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        actual = node.to_html()
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"

        self.assertEqual(actual, expected)

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parentnode_to_html_raises_value_error_with_none_tag(self):
        child_node = LeafNode("b", "grandchild")
        parent_node = ParentNode(None, [child_node])  # type: ignore

        fn = lambda: parent_node.to_html()
        _ = expected_error(self, fn, ValueError)

    def test_parentnode_to_html_raises_value_error_with_no_children(self):
        child_node = None
        parent_node = ParentNode("div", child_node)  # type: ignore

        fn = lambda: parent_node.to_html()
        _ = expected_error(self, fn, ValueError)

    def test_parentnode_to_html_raises_value_error_with_none_children(self):
        child_node = None
        parent_node = ParentNode("div", [child_node])  # type: ignore

        fn = lambda: parent_node.to_html()
        _ = expected_error(self, fn, ValueError)

    def test_full_dom(self):
        title_node = LeafNode("title", "My First HTML")
        meta_node = VoidNode("meta", {"charset": "UTF-8"})
        head_node = ParentNode("head", [title_node, meta_node])

        h2_node = LeafNode("h2", "London")
        p_node = LeafNode(
            "p",
            "CSS styles are added to make it easier to separate the divs, and to make them more pretty:)",
        )
        span_node = ParentNode("span", [h2_node, p_node])
        div_node = ParentNode(
            "div", [span_node], {"style": "background-color:#FFF4A3;"}
        )

        body_node = ParentNode("body", [div_node])
        html_node = ParentNode("html", [head_node, body_node])

        expected = """<html><head><title>My First HTML</title><meta charset="UTF-8"></head><body><div style="background-color:#FFF4A3;"><span><h2>London</h2><p>CSS styles are added to make it easier to separate the divs, and to make them more pretty:)</p></span></div></body></html>"""
        self.assertEqual(html_node.to_html(), expected)


if __name__ == "__main__":
    unittest.main()
