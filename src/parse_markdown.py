import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNDORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    """It takes a raw Markdown string (representing a full document) as input and returns a list of "block" strings."""
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
    if not isinstance(md, str):
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


def extract_markdown_images(text: str) -> list[tuple[str, str, str]]:
    # pat = r"!\[(.*?)\]\((.*?)\)"
    pat = r"(?P<image>!\[(?P<alt_text>.*?)\]\((?P<url>.*?)\))"
    matches = re.finditer(pat, text)
    results: list[tuple[str, str, str]] = []
    for match in matches:
        result = (match.group("alt_text"), match.group("url"), match.group("image"))
        results.append(result)
    return results


def extract_markdown_links(text: str) -> list[tuple[str, str, str]]:
    # pat = r"(?<!pattern)\[(.*?)\]\((.*?)\)"
    pat = r"(?<!\!)(?P<link>\[(?P<alt_text>.*?)\]\((?P<url>.*?)\))"
    matches = re.finditer(pat, text)
    results: list[tuple[str, str, str]] = []
    for match in matches:
        result = (match.group("alt_text"), match.group("url"), match.group("link"))
        results.append(result)
    return results


def extract_title(md: str) -> str:
    if not isinstance(md, str):
        raise TypeError("The supplied markdown must be a string.")

    for block in markdown_to_blocks(md):
        if is_title(block):
            return block[2:]

    raise ValueError("The markdown is missing a title")


def is_title(md: str) -> bool:
    pat = r"#{1} [\w\d\s]+"
    match = re.fullmatch(pat, md)
    return True if match else False


def is_heading(md: str) -> bool:
    pat = r"#{1,6} [\w\d\s]+"
    match = re.fullmatch(pat, md)
    return True if match else False


def is_code(md: str) -> bool:
    pat = r"```\n[\s\S]*```"
    match = re.fullmatch(pat, md)
    return True if match else False


def is_quote(md: str) -> bool:
    # pat = r">.*"
    # match = re.fullmatch(pat, md)
    return "\n".join(re.findall(r">.*", md)) == md


def is_unordered_list(md: str) -> bool:
    pat = r"\A(?:(- .*)\n{0,1})*\n{0,1}"
    match = re.fullmatch(pat, md)
    return True if match else False


def is_ordered_list(md: str) -> bool:
    lines = md.split("\n")
    line_num = 1
    for line in lines:
        prefix = f"{line_num}. "
        if line[: len(prefix)] == prefix:
            line_num += 1
        else:
            return False
    return True
