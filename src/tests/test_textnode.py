import unittest

from tests.utils import expected_error

from src.textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_with_upper_text_case(self):
        node = TextNode("This is a text node".upper(), TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_diff_text_case(self):
        node = TextNode("This is text node".upper(), TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_url_defaults_None(self):
        node = TextNode("This is text node".upper(), TextType.BOLD)
        self.assertIsNone(node.url)

    def test_not_eq_diff_typs(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text(self):
        text_node_to_html_node = TextNode.text_node_to_html_node

        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_repr(self):
        node = TextNode("hello", TextType.BOLD)
        self.assertEqual(repr(node), "TextNode(hello, bold, None)")

    def test_not_eq_diff_url(self):
        node = TextNode("same", TextType.LINK, url="https://example.com")
        node2 = TextNode("same", TextType.LINK, url="https://example.org")
        self.assertNotEqual(node, node2)

    def test_bold_to_html(self):
        node = TextNode("bold", TextType.BOLD)
        html_node = TextNode.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "bold")

    def test_italic_to_html(self):
        node = TextNode("italic", TextType.ITALIC)
        html_node = TextNode.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "italic")

    def test_code_to_html(self):
        node = TextNode("code", TextType.CODE)
        html_node = TextNode.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "code")

    def test_link_to_html_with_url(self):
        node = TextNode("Boot.dev", TextType.LINK, url="https://boot.dev")
        html_node = TextNode.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Boot.dev")
        self.assertEqual(html_node.props, {"href": "https://boot.dev"})

    def test_link_raises_without_url(self):
        node = TextNode("Boot.dev", TextType.LINK)

        fn = lambda: TextNode.text_node_to_html_node(node)
        cm = expected_error(self, fn, ValueError)
        self.assertEqual(str(cm.exception), "links must have a url")

    def test_image_to_html_with_url(self):
        node = TextNode("alt text", TextType.IMAGE, url="https://example.com/image.png")
        html_node = TextNode.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://example.com/image.png", "alt": "alt text"},
        )

    def test_image_raises_without_url(self):
        node = TextNode("alt text", TextType.IMAGE)

        fn = lambda: TextNode.text_node_to_html_node(node)
        cm = expected_error(self, fn, ValueError)
        self.assertEqual(str(cm.exception), "images must have a url")

    def test_invalid_text_type_raises(self):
        node = TextNode("x", TextType.TEXT)
        node.text_type = "not-a-texttype"  # type: ignore[assignment]

        fn = lambda: TextNode.text_node_to_html_node(node)
        cm = expected_error(self, fn, ValueError)
        self.assertIn("invalid TextType", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
