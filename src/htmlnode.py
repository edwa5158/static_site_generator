from __future__ import annotations

from typing import Optional, Sequence

from html_tags import HTMLTags


class HTMLNode:

    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        children: Optional[Sequence[HTMLNode]] = None,
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
            result += f"\tself.children = {self.children},\n"
        else:
            result += f"\tself.children = None,\n"
        if self.props:
            result += f"\tself.props = {self.props}\n"
        else:
            result += "\tself.props = None\n"

        result += ")"
        return result

    def to_html(self) -> str:
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
        for prop, value in self.props.items():
            result = " ".join([result, f'{prop}="{value}"'])

        return result

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, HTMLNode):
            return NotImplemented
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.props == other.props
            and self.children == other.children
        )
