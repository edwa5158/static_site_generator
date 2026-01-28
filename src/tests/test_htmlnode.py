import unittest

from html_tags import HTMLTags
from htmlnode import HTMLNode
from tests.utils import expected_error


class TestHTMLNode(unittest.TestCase):

    def test_props_to_html(self):
        props1 = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode(props=props1)
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)

    def test_to_html_raises_not_implemented(self):
        expected_error(self, lambda: HTMLNode().to_html(), NotImplementedError)

    def test_repr(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        expected = (
            "HTMLNode(\n"
            "\tself.tag = 'a',\n"
            "\tself.value = 'a link',\n"
            "\tself.children = None,\n"
            "\tself.props = {'href': 'https://www.google.com', 'target': '_blank'}\n"
            ")"
        )
        actual = repr(HTMLNode(tag="a", value="a link", props=props))
        self.assertEqual(expected, actual)

    def test_repr_no_children_no_props(self):
        expected = (
            "HTMLNode(\n"
            "\tself.tag = None,\n"
            "\tself.value = None,\n"
            "\tself.children = None,\n"
            "\tself.props = None\n"
            ")"
        )
        self.assertEqual(expected, repr(HTMLNode()))

    def test_repr_with_children_no_props(self):
        child = HTMLNode(tag="span", value="x")
        node = HTMLNode(tag="div", children=[child])
        expected = (
            "HTMLNode(\n"
            "\tself.tag = 'div',\n"
            "\tself.value = None,\n"
            f"\tself.children = {repr([child])},\n"
            "\tself.props = None\n"
            ")"
        )
        self.assertEqual(expected, repr(node))

    def test_props_to_html_empty_when_props_none(self):
        self.assertEqual(HTMLNode().props_to_html(), "")

    def test_props_to_html_empty_when_props_empty_dict(self):
        self.assertEqual(HTMLNode(props={}).props_to_html(), "")

    def test_to_html_helper_without_props(self):
        node = HTMLNode()
        self.assertEqual(
            node._to_html_helper(HTMLTags.PARAGRAPH, "hello", None),
            "<p>hello</p>",
        )

    def test_to_html_helper_with_props_on_node(self):
        node = HTMLNode(props={"class": "c", "id": "x"})
        self.assertEqual(
            node._to_html_helper(HTMLTags.PARAGRAPH, "hello", node.props),
            '<p class="c" id="x">hello</p>',
        )

    def test_to_html_helper_meta_closing_tag_empty(self):
        node = HTMLNode(props={"charset": "utf-8"})
        self.assertEqual(
            node._to_html_helper(HTMLTags.META, "", node.props),
            '<meta charset="utf-8">',
        )

    def test_eq_identical_nodes(self):
        props = {"href": "https://example.com", "target": "_blank"}
        children = [HTMLNode(tag="b", value="bold"), HTMLNode(tag=None, value=" text")]
        a = HTMLNode(tag="p", value=None, props=props, children=children)
        b = HTMLNode(
            tag="p",
            value=None,
            props={"href": "https://example.com", "target": "_blank"},
            children=[
                HTMLNode(tag="b", value="bold"),
                HTMLNode(tag=None, value=" text"),
            ],
        )
        self.assertEqual(a, b)

    def test_eq_tag_differs(self):
        a = HTMLNode(tag="p", value="x")
        b = HTMLNode(tag="div", value="x")
        self.assertNotEqual(a, b)

    def test_eq_value_differs(self):
        a = HTMLNode(tag="p", value="x")
        b = HTMLNode(tag="p", value="y")
        self.assertNotEqual(a, b)

    def test_eq_props_differs(self):
        a = HTMLNode(tag="a", value="link", props={"href": "https://a"})
        b = HTMLNode(tag="a", value="link", props={"href": "https://b"})
        self.assertNotEqual(a, b)

    def test_eq_children_differs_by_length(self):
        a = HTMLNode(tag="p", children=[HTMLNode(tag=None, value="x")])
        b = HTMLNode(
            tag="p",
            children=[HTMLNode(tag=None, value="x"), HTMLNode(tag=None, value="y")],
        )
        self.assertNotEqual(a, b)

    def test_eq_children_differs_by_order(self):
        child1 = HTMLNode(tag=None, value="x")
        child2 = HTMLNode(tag=None, value="y")
        a = HTMLNode(tag="p", children=[child1, child2])
        b = HTMLNode(tag="p", children=[child2, child1])
        self.assertNotEqual(a, b)

    def test_eq_children_same_structure(self):
        a = HTMLNode(
            tag="div",
            children=[
                HTMLNode(tag="span", value="a"),
                HTMLNode(tag="span", value="b", props={"class": "x"}),
            ],
        )
        b = HTMLNode(
            tag="div",
            children=[
                HTMLNode(tag="span", value="a"),
                HTMLNode(tag="span", value="b", props={"class": "x"}),
            ],
        )
        self.assertEqual(a, b)

    def test_eq_raises_when_other_is_not_htmlnode(self):
        # expected_error(self, lambda: HTMLNode(tag="p") == object(), NotImplemented)
        self.assertFalse(HTMLNode(tag="p") == object())
        self.assertFalse(object() == HTMLNode(tag="p"))


if __name__ == "__main__":
    unittest.main()
