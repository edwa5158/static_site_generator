from __future__ import annotations

from enum import Enum
from typing import Optional

from src.html_tags import HTMLTags


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

    def _to_html_helper(self, tag: HTMLTags, value: str, props: dict | None) -> str:
        result = tag.opening_tag()
        if props:
            result = result.replace(">", f"{self.props_to_html()}>")
        result += value + tag.closing_tag()
        return result

    def props_to_html(self):
        if not self.props:
            return ""

        result = ""
        for key, value in self.props.items():
            result = " ".join([result, f'{key}="{value}"'])

        return result
