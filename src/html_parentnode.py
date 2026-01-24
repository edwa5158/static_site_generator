from src.html_tags import HTMLTags
from src.htmlnode import HTMLNode
from typing import Sequence

class ParentNode(HTMLNode):
    def __init__(
        self, tag: str, children: Sequence[HTMLNode], props: dict[str, str] | None = None
    ) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("parrent node is missing tag")
        if not self.children:
            raise ValueError("parent is missing children")

        tag = HTMLTags(self.tag)
        value = self._to_html_helper(tag, "{{{}}}", self.props)
        child_value = ""
        for child in self.children:
            if child is None or not isinstance(child, HTMLNode):
                raise ValueError("child is not")
            child_value += child.to_html()

        value = value.replace("{{{}}}", child_value)
        return value
