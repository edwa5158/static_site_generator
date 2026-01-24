import unittest

from src.markdown_to_html import text_to_children


def _render_children(children) -> str:
    return "".join(child.to_html() for child in children)


def _simplify_children(children):
    return [
        {
            "tag": child.tag,
            "value": child.value,
            "props": child.props,
        }
        for child in children
    ]


class TestTextToHTML(unittest.TestCase):
    def _assert_case(self, md: str, expected, expected_html: str):
        children = text_to_children(md)
        self.assertEqual(_simplify_children(children), expected)
        self.assertEqual(_render_children(children), expected_html)

    def test_plain_text(self):
        self._assert_case(
            "Hello world",
            [{"tag": None, "value": "Hello world", "props": None}],
            "Hello world",
        )

    def test_bold_inline(self):
        self._assert_case(
            "A **bold** word",
            [
                {"tag": None, "value": "A ", "props": None},
                {"tag": "b", "value": "bold", "props": None},
                {"tag": None, "value": " word", "props": None},
            ],
            "A <b>bold</b> word",
        )

    def test_italic_inline(self):
        self._assert_case(
            "A _small_ word",
            [
                {"tag": None, "value": "A ", "props": None},
                {"tag": "i", "value": "small", "props": None},
                {"tag": None, "value": " word", "props": None},
            ],
            "A <i>small</i> word",
        )

    def test_code_inline(self):
        self._assert_case(
            "Use `print()` now",
            [
                {"tag": None, "value": "Use ", "props": None},
                {"tag": "code", "value": "print()", "props": None},
                {"tag": None, "value": " now", "props": None},
            ],
            "Use <code>print()</code> now",
        )

    def test_mixed_bold_italic_code(self):
        self._assert_case(
            "This has **bold**, _italic_, and `code`.",
            [
                {"tag": None, "value": "This has ", "props": None},
                {"tag": "b", "value": "bold", "props": None},
                {"tag": None, "value": ", ", "props": None},
                {"tag": "i", "value": "italic", "props": None},
                {"tag": None, "value": ", and ", "props": None},
                {"tag": "code", "value": "code", "props": None},
                {"tag": None, "value": ".", "props": None},
            ],
            "This has <b>bold</b>, <i>italic</i>, and <code>code</code>.",
        )

    def test_multiple_bold_segments(self):
        self._assert_case(
            "A **b1** and **b2**.",
            [
                {"tag": None, "value": "A ", "props": None},
                {"tag": "b", "value": "b1", "props": None},
                {"tag": None, "value": " and ", "props": None},
                {"tag": "b", "value": "b2", "props": None},
                {"tag": None, "value": ".", "props": None},
            ],
            "A <b>b1</b> and <b>b2</b>.",
        )

    def test_link(self):
        self._assert_case(
            "Go to [Boot.dev](https://boot.dev) now.",
            [
                {"tag": None, "value": "Go to ", "props": None},
                {
                    "tag": "a",
                    "value": "Boot.dev",
                    "props": {"href": "https://boot.dev"},
                },
                {"tag": None, "value": " now.", "props": None},
            ],
            'Go to <a href="https://boot.dev">Boot.dev</a> now.',
        )

    def test_two_adjacent_links(self):
        self._assert_case(
            "[A](u)[B](v)",
            [
                {"tag": "a", "value": "A", "props": {"href": "u"}},
                {"tag": "a", "value": "B", "props": {"href": "v"}},
            ],
            '<a href="u">A</a><a href="v">B</a>',
        )

    def test_image(self):
        self._assert_case(
            "Look ![cat](https://img/cat.png) here.",
            [
                {"tag": None, "value": "Look ", "props": None},
                {
                    "tag": "img",
                    "value": "",
                    "props": {"src": "https://img/cat.png", "alt": "cat"},
                },
                {"tag": None, "value": " here.", "props": None},
            ],
            'Look <img src="https://img/cat.png" alt="cat"></img> here.',
        )

    def test_two_adjacent_images(self):
        self._assert_case(
            "![a](u)![b](v)",
            [
                {"tag": "img", "value": "", "props": {"src": "u", "alt": "a"}},
                {"tag": "img", "value": "", "props": {"src": "v", "alt": "b"}},
            ],
            '<img src="u" alt="a"></img><img src="v" alt="b"></img>',
        )

    def test_image_plus_link(self):
        self._assert_case(
            "![alt](img) and [link](u)",
            [
                {"tag": "img", "value": "", "props": {"src": "img", "alt": "alt"}},
                {"tag": None, "value": " and ", "props": None},
                {"tag": "a", "value": "link", "props": {"href": "u"}},
            ],
            '<img src="img" alt="alt"></img> and <a href="u">link</a>',
        )

    def test_unmatched_bold_delimiter(self):
        self._assert_case(
            "A **bold B",
            [
                {"tag": None, "value": "A ", "props": None},
                {"tag": "b", "value": "bold B", "props": None},
            ],
            "A <b>bold B</b>",
        )

    def test_bold_containing_link_markup(self):
        self._assert_case(
            "A **[x](u)** B",
            [
                {"tag": None, "value": "A ", "props": None},
                {"tag": "b", "value": "[x](u)", "props": None},
                {"tag": None, "value": " B", "props": None},
            ],
            "A <b>[x](u)</b> B",
        )

    def test_newlines_preserved(self):
        self._assert_case(
            "Line1\nLine2",
            [{"tag": None, "value": "Line1\nLine2", "props": None}],
            "Line1\nLine2",
        )

    def test_code_plus_image_plus_punctuation(self):
        self._assert_case(
            "A `code` and ![i](u).",
            [
                {"tag": None, "value": "A ", "props": None},
                {"tag": "code", "value": "code", "props": None},
                {"tag": None, "value": " and ", "props": None},
                {"tag": "img", "value": "", "props": {"src": "u", "alt": "i"}},
                {"tag": None, "value": ".", "props": None},
            ],
            'A <code>code</code> and <img src="u" alt="i"></img>.',
        )

    def test_unicode_text(self):
        self._assert_case(
            "Café **naïve**.",
            [
                {"tag": None, "value": "Café ", "props": None},
                {"tag": "b", "value": "naïve", "props": None},
                {"tag": None, "value": ".", "props": None},
            ],
            "Café <b>naïve</b>.",
        )
