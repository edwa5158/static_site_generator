import unittest

from src.html_leafnode import LeafNode
from src.html_parentnode import ParentNode
from src.markdown_to_html import blockquote_to_html as bq2html
from src.markdown_to_html import code_block_to_html as cb2html
from src.markdown_to_html import text_to_children as t2c
from tests.utils import expected_error


class TestTextToChildren(unittest.TestCase):
    def _render_children(self, children) -> str:
        return "".join(child.to_html() for child in children)

    def _simplify_children(self, children):
        return [
            {
                "tag": child.tag,
                "value": child.value,
                "props": child.props,
            }
            for child in children
        ]

    def _assert_case(self, md: str, expected, expected_html: str):
        children = t2c(md)
        self.assertEqual(self._simplify_children(children), expected)
        self.assertEqual(self._render_children(children), expected_html)

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


class TestCodeBlockToChildren(unittest.TestCase):
    def test_structure_simple(self):
        md_text: str = "print('hi')"
        node = cb2html(md_text)

        self.assertIsInstance(node, ParentNode)
        self.assertEqual(node.tag, "pre")
        self.assertIsNone(node.props)
        self.assertIsNotNone(node.children)
        self.assertEqual(len(node.children), 1)

        child = node.children[0]
        self.assertIsInstance(child, LeafNode)
        self.assertEqual(child.tag, "code")
        self.assertEqual(child.value, "print('hi')")
        self.assertIsNone(child.props)

        self.assertEqual(node.to_html(), "<pre><code>print('hi')</code></pre>")

    def test_multiline_preserved(self):
        text = "line1\nline2\n"
        node = cb2html(text)
        self.assertEqual(node.to_html(), f"<pre><code>{text}</code></pre>")

    def test_includes_fence_markers_if_present(self):
        text = "```\ncode\n```"
        node = cb2html(text)
        self.assertEqual(node.to_html(), f"<pre><code>{text}</code></pre>")

    def test_preserves_angle_brackets_no_escaping(self):
        text = "<b>not escaped</b>"
        node = cb2html(text)
        self.assertEqual(node.to_html(), "<pre><code><b>not escaped</b></code></pre>")

    def test_whitespace_only_is_allowed(self):
        text = "   \n\t"
        node = cb2html(text)
        self.assertEqual(node.to_html(), f"<pre><code>{text}</code></pre>")

    def test_empty_string_raises_on_render(self):
        fn = lambda: cb2html(None).to_html()  # type: ignore
        cm = expected_error(self, fn, ValueError)
        self.assertEqual(str(cm.exception), "leaf node has no value")


class TestBlockQuoteToHTML(unittest.TestCase):
    def _render(self, node) -> str:
        return node.to_html()

    def _simplify_children(self, node):
        return [
            {"tag": child.tag, "value": child.value, "props": child.props}
            for child in node.children  # type: ignore[attr-defined]
        ]

    def test_blockquote_node_structure_simple_text(self):
        node = bq2html("Hello quote")

        from src.html_parentnode import ParentNode

        self.assertIsInstance(node, ParentNode)
        self.assertEqual(node.tag, "blockquote")
        self.assertIsNone(node.props)
        self.assertIsNotNone(node.children)
        self.assertEqual(self._render(node), "<blockquote>Hello quote</blockquote>")

        simplified = self._simplify_children(node)
        self.assertEqual(
            simplified,
            [{"tag": None, "value": "Hello quote", "props": None}],
        )

    def test_blockquote_preserves_newlines(self):
        node = bq2html("Line1\nLine2")
        self.assertEqual(self._render(node), "<blockquote>Line1\nLine2</blockquote>")

    def test_blockquote_mixed_bold_italic_code(self):
        node = bq2html("This has **bold**, _italic_, and `code`.")
        self.assertEqual(
            self._render(node),
            "<blockquote>This has <b>bold</b>, <i>italic</i>, and <code>code</code>.</blockquote>",
        )

    def test_blockquote_multiple_bold_segments(self):
        node = bq2html("A **b1** and **b2**.")
        self.assertEqual(
            self._render(node),
            "<blockquote>A <b>b1</b> and <b>b2</b>.</blockquote>",
        )

    def test_blockquote_contains_link(self):
        node = bq2html("Go to [Boot.dev](https://boot.dev) now.")
        self.assertEqual(
            self._render(node),
            '<blockquote>Go to <a href="https://boot.dev">Boot.dev</a> now.</blockquote>',
        )

    def test_blockquote_adjacent_links(self):
        node = bq2html("[A](u)[B](v)")
        self.assertEqual(
            self._render(node),
            '<blockquote><a href="u">A</a><a href="v">B</a></blockquote>',
        )

    def test_blockquote_contains_image(self):
        node = bq2html("Look ![cat](https://img/cat.png) here.")
        self.assertEqual(
            self._render(node),
            '<blockquote>Look <img src="https://img/cat.png" alt="cat"></img> here.</blockquote>',
        )

    def test_blockquote_adjacent_images(self):
        node = bq2html("![a](u)![b](v)")
        self.assertEqual(
            self._render(node),
            '<blockquote><img src="u" alt="a"></img><img src="v" alt="b"></img></blockquote>',
        )

    def test_blockquote_image_plus_link(self):
        node = bq2html("![alt](img) and [link](u)")
        self.assertEqual(
            self._render(node),
            '<blockquote><img src="img" alt="alt"></img> and <a href="u">link</a></blockquote>',
        )

    def test_blockquote_code_plus_image_plus_punctuation(self):
        node = bq2html("A `code` and ![i](u).")
        self.assertEqual(
            self._render(node),
            '<blockquote>A <code>code</code> and <img src="u" alt="i"></img>.</blockquote>',
        )

    def test_blockquote_unmatched_bold_delimiter(self):
        node = bq2html("A **bold B")
        self.assertEqual(
            self._render(node),
            "<blockquote>A <b>bold B</b></blockquote>",
        )

    def test_blockquote_bold_containing_link_markup_is_not_nested(self):
        node = bq2html("A **[x](u)** B")
        self.assertEqual(
            self._render(node),
            "<blockquote>A <b>[x](u)</b> B</blockquote>",
        )

    def test_blockquote_unicode_text(self):
        node = bq2html("Café **naïve**.")
        self.assertEqual(
            self._render(node),
            "<blockquote>Café <b>naïve</b>.</blockquote>",
        )

    def test_blockquote_invalid_input_raises(self):
        fn = lambda: bq2html(None)  # type: ignore
        expected_error(self, fn, TypeError)


# ...existing code...

if __name__ == "__main__":
    unittest.main()
