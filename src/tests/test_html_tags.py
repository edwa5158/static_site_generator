import unittest

from src.html_tags import HTMLTags
from tests.utils import expected_error


class TestHTMLTags(unittest.TestCase):
    def test_enum_values(self):
        self.assertEqual(HTMLTags.HTML.value, "html")
        self.assertEqual(HTMLTags.BODY.value, "body")
        self.assertEqual(HTMLTags.HEAD.value, "head")
        self.assertEqual(HTMLTags.PARAGRAPH.value, "p")
        self.assertEqual(HTMLTags.ANCHOR.value, "a")
        self.assertEqual(HTMLTags.IMAGE.value, "img")
        self.assertEqual(HTMLTags.UNORDERED_LIST.value, "ul")
        self.assertEqual(HTMLTags.ORDERED_LIST.value, "ol")
        self.assertEqual(HTMLTags.LIST_ITEM.value, "li")
        self.assertEqual(HTMLTags.BOLD.value, "b")
        self.assertEqual(HTMLTags.ITALICS.value, "i")
        self.assertEqual(HTMLTags.SPAN.value, "span")
        self.assertEqual(HTMLTags.DIV.value, "div")
        self.assertEqual(HTMLTags.META.value, "meta")
        self.assertEqual(HTMLTags.TITLE.value, "title")
        self.assertEqual(HTMLTags.H1.value, "h1")
        self.assertEqual(HTMLTags.H2.value, "h2")
        self.assertEqual(HTMLTags.H3.value, "h3")
        self.assertEqual(HTMLTags.H4.value, "h4")
        self.assertEqual(HTMLTags.H5.value, "h5")
        self.assertEqual(HTMLTags.H6.value, "h6")

    def test_opening_tag_all_members(self):
        self.assertEqual(HTMLTags.HTML.opening_tag(), "<html>")
        self.assertEqual(HTMLTags.BODY.opening_tag(), "<body>")
        self.assertEqual(HTMLTags.HEAD.opening_tag(), "<head>")
        self.assertEqual(HTMLTags.PARAGRAPH.opening_tag(), "<p>")
        self.assertEqual(HTMLTags.ANCHOR.opening_tag(), "<a>")
        self.assertEqual(HTMLTags.IMAGE.opening_tag(), "<img>")
        self.assertEqual(HTMLTags.UNORDERED_LIST.opening_tag(), "<ul>")
        self.assertEqual(HTMLTags.ORDERED_LIST.opening_tag(), "<ol>")
        self.assertEqual(HTMLTags.LIST_ITEM.opening_tag(), "<li>")
        self.assertEqual(HTMLTags.BOLD.opening_tag(), "<b>")
        self.assertEqual(HTMLTags.ITALICS.opening_tag(), "<i>")
        self.assertEqual(HTMLTags.SPAN.opening_tag(), "<span>")
        self.assertEqual(HTMLTags.DIV.opening_tag(), "<div>")
        self.assertEqual(HTMLTags.META.opening_tag(), "<meta>")
        self.assertEqual(HTMLTags.TITLE.opening_tag(), "<title>")
        self.assertEqual(HTMLTags.H1.opening_tag(), "<h1>")
        self.assertEqual(HTMLTags.H2.opening_tag(), "<h2>")
        self.assertEqual(HTMLTags.H3.opening_tag(), "<h3>")
        self.assertEqual(HTMLTags.H4.opening_tag(), "<h4>")
        self.assertEqual(HTMLTags.H5.opening_tag(), "<h5>")
        self.assertEqual(HTMLTags.H6.opening_tag(), "<h6>")

    def test_closing_tag_all_members(self):
        self.assertEqual(HTMLTags.HTML.closing_tag(), "</html>")
        self.assertEqual(HTMLTags.BODY.closing_tag(), "</body>")
        self.assertEqual(HTMLTags.HEAD.closing_tag(), "</head>")
        self.assertEqual(HTMLTags.PARAGRAPH.closing_tag(), "</p>")
        self.assertEqual(HTMLTags.ANCHOR.closing_tag(), "</a>")
        self.assertEqual(HTMLTags.IMAGE.closing_tag(), "</img>")
        self.assertEqual(HTMLTags.UNORDERED_LIST.closing_tag(), "</ul>")
        self.assertEqual(HTMLTags.ORDERED_LIST.closing_tag(), "</ol>")
        self.assertEqual(HTMLTags.LIST_ITEM.closing_tag(), "</li>")
        self.assertEqual(HTMLTags.BOLD.closing_tag(), "</b>")
        self.assertEqual(HTMLTags.ITALICS.closing_tag(), "</i>")
        self.assertEqual(HTMLTags.SPAN.closing_tag(), "</span>")
        self.assertEqual(HTMLTags.DIV.closing_tag(), "</div>")
        self.assertEqual(HTMLTags.META.closing_tag(), "")
        self.assertEqual(HTMLTags.TITLE.closing_tag(), "</title>")
        self.assertEqual(HTMLTags.H1.closing_tag(), "</h1>")
        self.assertEqual(HTMLTags.H2.closing_tag(), "</h2>")
        self.assertEqual(HTMLTags.H3.closing_tag(), "</h3>")
        self.assertEqual(HTMLTags.H4.closing_tag(), "</h4>")
        self.assertEqual(HTMLTags.H5.closing_tag(), "</h5>")
        self.assertEqual(HTMLTags.H6.closing_tag(), "</h6>")

    def test_opening_tag_invalid_raises(self):
        expected_error(self, lambda: HTMLTags.opening_tag("not-a-tag"), ValueError)  # type: ignore

    def test_closing_tag_invalid_raises(self):
        expected_error(self, lambda: HTMLTags.closing_tag("not-a-tag"), ValueError)  # type: ignore


if __name__ == "__main__":
    unittest.main()
