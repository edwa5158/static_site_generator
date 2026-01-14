import unittest

from src.markdown_to_textnode import split_nodes_delimiter
from src.textnode import TextNode, TextType


class TestMarkdownToTextNode(unittest.TestCase):

    def test_simple_code_conversion(self):
        node = TextNode("`2**3`", TextType.TEXT)
        actual = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("", TextType.TEXT, None),
            TextNode("2**3", TextType.CODE, None),
            TextNode("", TextType.TEXT, None),
        ]
        self.assertEqual(actual, expected)

    def test_another_code_conversion(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        actual = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(actual, expected)

    def test_simple_bold_conversion(self):
        node = TextNode("shouldn't be **should be** shouldn't be", TextType.TEXT)
        actual = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("shouldn't be ", TextType.TEXT, None),
            TextNode("should be", TextType.BOLD, None),
            TextNode(" shouldn't be", TextType.TEXT, None),
        ]
        self.assertEqual(actual, expected)

    def test_bold_in_bold_out(self):
        node = TextNode("shouldn't be **should be** shouldn't be", TextType.BOLD)
        actual = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [node]
        self.assertEqual(actual, expected)

    def test_simple_italic_conversion(self):
        node = TextNode("shouldn't be _should be_ shouldn't be", TextType.TEXT)
        actual = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("shouldn't be ", TextType.TEXT, None),
            TextNode("should be", TextType.ITALIC, None),
            TextNode(" shouldn't be", TextType.TEXT, None),
        ]
        self.assertEqual(actual, expected)

    def test_raises_value_error_with_none_nodes(self):

        with self.assertRaises(ValueError) as cm:
            _ = split_nodes_delimiter(None, "`", TextType.CODE)  # type: ignore

        if type(cm.exception) is not NotImplementedError:
            print(f"different exception type detected: {type(cm.exception)}")
            print(f"{cm.exception.__traceback__ = }")

    def test_raises_value_error_with_mismatched_node_type(self):

        with self.assertRaises(ValueError) as cm:
            _ = split_nodes_delimiter([TextNode("some text", TextType.BOLD, None)], "`", TextType.BOLD)  # type: ignore

        if type(cm.exception) is not NotImplementedError:
            print(f"different exception type detected: {type(cm.exception)}")
            print(f"{cm.exception.__traceback__ = }")

    def test_raises_value_error_with_unsupported_node_type(self):

        with self.assertRaises(ValueError) as cm:
            _ = split_nodes_delimiter([TextNode("some text", TextType.IMAGE, url="your/mom.jpeg")], "image", TextType.IMAGE)  # type: ignore

        if type(cm.exception) is not NotImplementedError:
            print(f"different exception type detected: {type(cm.exception)}")
            print(f"{cm.exception.__traceback__ = }")
