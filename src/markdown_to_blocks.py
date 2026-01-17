from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNDORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

    @staticmethod
    def delimiters():
        result: list[str] = []
        # paragraph
        # None - matches this as the default
        # headings
        result.extend(["#" * i + " " for i in range(1, 7)])
        # code
        result.append("```" + "\n")
        # quote

        # unordered_list

        # ordered_list


def markdown_to_blocks(markdown: str) -> list[str]:
    if not type(markdown) is str:
        raise TypeError(f"invalid input type {type(markdown)}; only strings accepted")

    initial_blocks: list[str] = markdown.split("\n\n")
    blocks: list[str] = []
    for block in initial_blocks:
        block = block.strip()
        if len(block) > 0:
            blocks.append(block)
    return blocks


def block_to_block_type(md: str) -> BlockType:
    from src.regexes import (
        is_code,
        is_heading,
        is_ordered_list,
        is_quote,
        is_unordered_list,
    )

    if type(md) is not str:
        raise TypeError(f"invalid input type: {type(md)}, only str type accepted.")
    

    if is_heading(md):
        return BlockType.HEADING
    elif is_code(md):
        return BlockType.CODE
    elif is_quote(md):
        return BlockType.QUOTE
    elif is_unordered_list(md):
        return BlockType.UNDORDERED_LIST
    elif is_ordered_list(md):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
