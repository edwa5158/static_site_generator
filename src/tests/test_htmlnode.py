import unittest

from src.htmlnode import HTMLNode


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
        node = HTMLNode()

        with self.assertRaises(NotImplementedError) as cm:
            node.to_html()

        if type(cm.exception) is not NotImplementedError:
            self.fail(
                f"different exception type detected: {type(cm.exception)}"
                + f"{cm.exception.__traceback__ = }"
            )

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


if __name__ == "__main__":
    unittest.main()
