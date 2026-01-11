from __future__ import annotations

from typing import Optional
from enum import Enum


class HTMLNode:

    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        children: Optional[list[HTMLNode]] = None,
        props: Optional[dict[str, str]] = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self) -> str:
        result = f"HTMLNode(\n"
        result += f"\t{self.tag = },\n"
        result += f"\t{self.value = },\n"

        if self.children:
            print("self.children = true")
            result += f"\tself.children = {self.children},\n"
        else:
            result += f"\tself.children = None,\n"
        if self.props:
            result += f"\tself.props = {self.props}\n"
        else:
            result += "\tself.props = None\n"

        result += ")"
        return result

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if not self.props:
            return ""

        result = ""
        for key, value in self.props.items():
            result = " ".join([result, f'{key}="{value}"'])

        return result


class LeafNode(HTMLNode):
    def __init__(
        self, tag: str | None, value: str, props: dict[str, str] | None = None
    ) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("leaf node has no value")
        if not self.tag:
            return self.value
        else:
