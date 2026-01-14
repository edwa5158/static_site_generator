from enum import Enum
from typing import Literal, TypeAlias, TypeVar

from src.textnode import TextNode, TextType


class Delimiter(Enum):
    BOLD = "**"
    ITALIC = "_"
    CODE = "`"


def delimiter_doesnt_match(text_type: TextType, delimiter: str) -> bool:
    match text_type:
        case TextType.BOLD:
            return delimiter != Delimiter.BOLD.value
        case TextType.ITALIC:
            return delimiter != Delimiter.ITALIC.value
        case TextType.CODE:
            return delimiter != Delimiter.CODE.value
        case _:
            raise ValueError("Unsupported text type")


def split_nodes_delimiter(
    old_nodes: list[TextNode],
    delimiter: Literal[
        "**",
        "_",
        "`",
    ],
    text_type: TextType,
) -> list[TextNode]:
    """
    Converts a list of `TextNode` objects (`old_nodes`) of the type `TextType.TEXT` to the appropriate `TextType` based on the `delimiter` and `text_type` parameter passed.
    Does NOT support nested inline elements (e.g., "*this text has **bold** nested in italics*)
    """

    if not old_nodes:
        raise ValueError("`old_nodes` cannot be empty or None")

    if delimiter_doesnt_match(text_type, delimiter):
        raise ValueError("the text_type and delimiter are incompatible or incorrect")

    new_nodes: list[TextNode] = []

    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            # We only convert TextType.TEXT
            new_nodes.append(node)
            continue

        text_parts: list[str] = node.text.split(delimiter)
        opened: bool = False
        for part in text_parts:
            if opened:
                new_nodes.append(TextNode(part, text_type, node.url))
                opened = False
            else:
                new_nodes.append(TextNode(part, TextType.TEXT, node.url))
                opened = True
    return new_nodes
