import unittest

from src.parse_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    extract_title,
)
from src.tests.utils import expected_error


class TestExtractMarkdownImages(unittest.TestCase):

    def test_single_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        actual = extract_markdown_images(text)
        expected = [
            (
                "rick roll",
                "https://i.imgur.com/aKaOqIh.gif",
                "![rick roll](https://i.imgur.com/aKaOqIh.gif)",
            ),
            (
                "obi wan",
                "https://i.imgur.com/fJRm4Vk.jpeg",
                "![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            ),
        ]
        self.assertEqual(actual, expected)


class TestExtractLinks(unittest.TestCase):

    def test_single_image(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        actual = extract_markdown_links(text)
        expected = [
            (
                "to boot dev",
                "https://www.boot.dev",
                "[to boot dev](https://www.boot.dev)",
            ),
            (
                "to youtube",
                "https://www.youtube.com/@bootdotdev",
                "[to youtube](https://www.youtube.com/@bootdotdev)",
            ),
        ]
        self.assertEqual(actual, expected)


class TestExtractTitle(unittest.TestCase):
    def test_happy_path(self):
        md = "# A nice title\n\nSome text"
        title = extract_title(md)
        expected = "A nice title"
        self.assertEqual(title, expected)

    def test_missing_title(self):
        md = "## a heading\n\n### another heading\n\na paragraph"
        _ = expected_error(self, lambda: extract_title(md), ValueError)

    def test_wrong_input_type(self):
        md = 3
        _ = expected_error(self, lambda: extract_title(md), TypeError)  # type: ignore

    def test_with_title_later_in_doc(self):
        md = "some text\n\n# a title"
        title = extract_title(md)
        expected = "a title"
        self.assertEqual(title, expected)


if __name__ == "__main__":
    unittest.main()
