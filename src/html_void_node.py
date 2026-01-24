from html_tags import HTMLTags
from htmlnode import HTMLNode


class VoidNode(HTMLNode):

    def __init__(self, tag: str, props: dict[str, str] | None = None) -> None:
        super().__init__(tag, None, None, props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("void element has no tag")
        else:
            tag = HTMLTags(self.tag)
            return self._to_html_helper(tag, "", self.props)
