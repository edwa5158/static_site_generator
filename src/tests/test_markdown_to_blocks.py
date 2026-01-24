import unittest

from src.markdown_to_blocks import BlockType, block_to_block_type as b2bt, markdown_to_blocks
from src.tests.utils import expected_error


class TestMarkdownToBlocks(unittest.TestCase):

    def test_happy_path(self):
        md: str = (
            "This is **bolded** paragraph\n\n"
            "This is another paragraph with _italic_ text and `code` here\n"
            "This is the same paragraph on a new line\n\n"
            "- This is a list\n"
            "- with items\n"
        )
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_empty_string(self):
        md: str = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [],
        )

    def test_none(self):
        expected_error(self, lambda: markdown_to_blocks(None), TypeError)  # type: ignore

    def test_int(self):
        expected_error(self, lambda: markdown_to_blocks(1), TypeError)  # type: ignore

    def test_md_without_blocks(self):
        md: str = "This is **bolded** paragraph"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["This is **bolded** paragraph"],
        )

    def test_md_with_empty_blocks(self):
        md: str = "This is **bolded** paragraph\n\n" + ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["This is **bolded** paragraph"],
        )

    def test_md_with_extra_line_breaks(self):
        md: str = (
            "This is **bolded** paragraph\n\n\n"
            "This is another paragraph with _italic_ text and `code` here\n"
            "This is the same paragraph on a new line\n\n\n"
            "- This is a list\n"
            "- with items\n"
        )
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_md_only_line_breaks_and_empty_strings(self):
        md: str = "" + "\n\n" + "" + "\n\n" + "" + "\n\n" "" + "\n\n" + "" + "\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [],
        )


class TestBlockToBlockType(unittest.TestCase):

    def test_happy_headings(self):
        heading1 = "# heading 1"
        heading2 = "## heading 2"
        heading3 = "### heading 3"
        heading4 = "#### heading 4"
        heading5 = "##### heading 5"
        heading6 = "###### heading 6"

        self.assertEqual(b2bt(heading1), BlockType.HEADING)
        self.assertEqual(b2bt(heading2), BlockType.HEADING)
        self.assertEqual(b2bt(heading3), BlockType.HEADING)
        self.assertEqual(b2bt(heading4), BlockType.HEADING)
        self.assertEqual(b2bt(heading5), BlockType.HEADING)
        self.assertEqual(b2bt(heading6), BlockType.HEADING)

    def test_happy_code(self):
        code = """```
    some code
    some more code
```"""

    def test_happy_quotes(self):
        quote = "< some quote here >"
        multi_line_quote = """<
        multi
        line
        quote
        >"""
        self.assertEqual(b2bt(quote), BlockType.QUOTE)
        self.assertEqual(b2bt(multi_line_quote), BlockType.QUOTE)

    def test_happy_unordered_list(self):
        unordered_list = "- first line\n- second line\n- third line"
        self.assertEqual(b2bt(unordered_list), BlockType.UNDORDERED_LIST)

    def test_happy_orderd_list(self):
        ordered_list = "1. first line\n2. second line\n3. third line"
        self.assertEqual(b2bt(ordered_list), BlockType.ORDERED_LIST)

    def test_happy_paragraph(self):
        paragraph = "a paragraph"
        self.assertEqual(b2bt(paragraph), BlockType.PARAGRAPH)

    def test_wrong_input_type_none(self):
        expected_error(self, lambda: b2bt(None), TypeError)  # type: ignore

    def test_wrong_input_type_int(self):
        expected_error(self, lambda: b2bt(int(3)), TypeError)  # type: ignore

    def test_heading_without_space(self):
        md = "#a bad heading"
        self.assertEqual(b2bt(md), BlockType.PARAGRAPH)

    def test_heading_with_leading_space(self):
        md = " #a bad heading"
        self.assertEqual(b2bt(md), BlockType.PARAGRAPH)

    def test_heading_with_extra_space(self):
        md = "#       a heading with lots of space"
        self.assertEqual(b2bt(md), BlockType.HEADING)

    def test_ordered_list_out_of_order(self):
        md = "1. first line \n3. second line \n2. third line"
        self.assertEqual(b2bt(md), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
