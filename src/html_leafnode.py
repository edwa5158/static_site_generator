from html_tags import HTMLTags
from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(
        self, tag: str | None, value: str, props: dict[str, str] | None = None
    ) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("leaf node has no value")
        if not self.tag:
            return self.value
        else:
            tag = HTMLTags(self.tag)
            return self._to_html_helper(tag, self.value, self.props)
