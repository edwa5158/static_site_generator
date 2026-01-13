from __future__ import annotations

from enum import Enum
from typing import Optional


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(
        self, text: str, text_type: TextType, url: Optional[str] = None
    ) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: TextNode) -> bool:
        return (
            (self.text == other.text)
            and (self.text_type == other.text_type)
            and (self.url == other.url)
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

    @staticmethod
    def text_node_to_html_node(text_node: TextNode):
        from src.html_leafnode import LeafNode
        from src.htmlnode import HTMLNode

        match text_node.text_type:
            case TextType.TEXT:
                return LeafNode(None, text_node.text)
            case TextType.BOLD:
                return LeafNode("b", text_node.text)
            case TextType.ITALIC:
                return LeafNode("i", text_node.text)
            case TextType.CODE:
                return LeafNode("code", text_node.text)
            case TextType.LINK:
                if not text_node.url:
                    raise ValueError("links must have a url")
                return LeafNode("a", text_node.text, {"href": text_node.url})
            case TextType.IMAGE:
                if not text_node.url:
                    raise ValueError("images must have a url")
                return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
            case _:
                raise ValueError(f"invalid TextType {text_node.text_type = }")
