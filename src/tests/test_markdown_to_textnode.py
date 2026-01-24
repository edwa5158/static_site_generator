import unittest

from src.markdown_to_textnode import split_nodes_delimiter as snbd
from src.markdown_to_textnode import (
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from src.textnode import TextNode, TextType
from tests.utils import expected_error


class TestMarkdownToTextNode(unittest.TestCase):

    def test_simple_code_conversion(self):
        node = TextNode("`2**3`", TextType.TEXT)
        actual = snbd([node], "`", TextType.CODE)
        expected = [
            TextNode("", TextType.TEXT, None),
            TextNode("2**3", TextType.CODE, None),
            TextNode("", TextType.TEXT, None),
        ]
        self.assertEqual(actual, expected)

    def test_another_code_conversion(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        actual = snbd([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(actual, expected)

    def test_simple_bold_conversion(self):
        node = TextNode("shouldn't be **should be** shouldn't be", TextType.TEXT)
        actual = snbd([node], "**", TextType.BOLD)
        expected = [
            TextNode("shouldn't be ", TextType.TEXT, None),
            TextNode("should be", TextType.BOLD, None),
            TextNode(" shouldn't be", TextType.TEXT, None),
        ]
        self.assertEqual(actual, expected)

    def test_bold_in_bold_out(self):
        node = TextNode("shouldn't be **should be** shouldn't be", TextType.BOLD)
        actual = snbd([node], "**", TextType.BOLD)
        expected = [node]
        self.assertEqual(actual, expected)

    def test_simple_italic_conversion(self):
        node = TextNode("shouldn't be _should be_ shouldn't be", TextType.TEXT)
        actual = snbd([node], "_", TextType.ITALIC)
        expected = [
            TextNode("shouldn't be ", TextType.TEXT, None),
            TextNode("should be", TextType.ITALIC, None),
            TextNode(" shouldn't be", TextType.TEXT, None),
        ]
        self.assertEqual(actual, expected)

    def test_raises_value_error_with_none_nodes(self):
        fn = lambda: snbd(None, "`", TextType.CODE)  # type: ignore
        expected_error(self, fn, ValueError)  # type: ignore

    def test_raises_value_error_with_mismatched_node_type(self):
        fn = lambda: snbd(
            [TextNode("some text", TextType.BOLD, None)], "`", TextType.BOLD
        )
        expected_error(self, fn, ValueError)

    def test_raises_value_error_with_unsupported_node_type(self):
        fn = lambda: snbd(
            [TextNode("some text", TextType.IMAGE, url="your/mom.jpeg")],
            "image",  # type: ignore
            TextType.IMAGE,
        )
        expected_error(self, fn, ValueError)


class TestSpliteNodesImage(unittest.TestCase):
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
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_with_a_link(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        link_node = TextNode("this is a link", TextType.LINK, url="")
        new_nodes = split_nodes_image([link_node, node])

        self.assertListEqual(
            [
                link_node,
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_with_text_after(self):
        old_nodes = [
            TextNode(
                " and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a ",
                TextType.TEXT,
                None,
            )
        ]
        expected = [
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(old_nodes)

        self.assertEqual(new_nodes, expected)


class TestSpliteNodesLink(unittest.TestCase):
    def test_split_links(self):

        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", TextType.TEXT, None),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_links_with_img(self):

        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        img_node = TextNode(
            "This is an image node",
            TextType.IMAGE,
            url="",
        )
        new_nodes = split_nodes_link([img_node, node])
        expected = [
            img_node,
            TextNode("This is text with a link ", TextType.TEXT, None),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertEqual(new_nodes, expected)


class TestTextToTextNode(unittest.TestCase):
    def test_text_conversion(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(expected, text_to_textnodes(text))


if __name__ == "__main__":
    unittest.main()
