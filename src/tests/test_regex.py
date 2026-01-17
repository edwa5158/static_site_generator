import unittest

from src.regexes import extract_markdown_images, extract_markdown_links

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

if __name__ == "__main__":
    unittest.main()
