import unittest

from src.markdown_to_blocks import BlockType, block_to_block_type, markdown_to_blocks


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
        with self.assertRaises(TypeError) as cm:
            _ = markdown_to_blocks(None)  # type: ignore

        if type(cm.exception) is not TypeError:
            self.fail(
                f"different exception type detected: {type(cm.exception)}"
                + f"{cm.exception.__traceback__ = }"
            )

    def test_int(self):
        with self.assertRaises(TypeError) as cm:
            _ = markdown_to_blocks(1)  # type: ignore

        if type(cm.exception) is not TypeError:
            self.fail(
                f"different exception type detected: {type(cm.exception)}"
                + f"{cm.exception.__traceback__ = }"
            )

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
    def test_happy_path(self):
        heading1 = "# heading 1"
        heading2 = "## heading 2"
        heading3 = "### heading 3"
        heading4 = "#### heading 4"
        heading5 = "##### heading 5"
        heading6 = "###### heading 6"

        code = """```
    some code
    some more code
```"""
        quote = "< some quote here >"
        multi_line_quote = """<
        multi
        line
        quote
        >"""
        unordered_list = "- first line\n- second line\n- third line"
        ordered_list = "1. first line\n2. second line\n3. third line"
        paragraph = "a paragraph"

        btbt = block_to_block_type

        self.assertEqual(btbt(heading1), BlockType.HEADING)
        self.assertEqual(btbt(heading2), BlockType.HEADING)
        self.assertEqual(btbt(heading3), BlockType.HEADING)
        self.assertEqual(btbt(heading4), BlockType.HEADING)
        self.assertEqual(btbt(heading5), BlockType.HEADING)
        self.assertEqual(btbt(heading6), BlockType.HEADING)

        self.assertEqual(btbt(code), BlockType.CODE)

        self.assertEqual(btbt(quote), BlockType.QUOTE)
        self.assertEqual(btbt(multi_line_quote), BlockType.QUOTE)

        self.assertEqual(btbt(unordered_list), BlockType.UNDORDERED_LIST)
        self.assertEqual(btbt(ordered_list), BlockType.ORDERED_LIST)

        self.assertEqual(btbt(paragraph), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
