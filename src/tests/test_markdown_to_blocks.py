import unittest

from src.markdown_to_blocks import markdown_to_blocks


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


if __name__ == "__main__":
    unittest.main()
