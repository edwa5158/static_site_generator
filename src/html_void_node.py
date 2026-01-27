from multiprocessing.sharedctypes import Value

from src.html_tags import HTMLTags
from src.htmlnode import HTMLNode


class VoidNode(HTMLNode):

    def __init__(self, tag: str, props: dict[str, str] | None = None) -> None:
        if not (tag and isinstance(tag, str)):
            raise ValueError("A void element must have a tag.")
        super().__init__(tag, None, None, props)

    def to_html(self) -> str:
        if not self.tag or self.tag is None:
            raise ValueError("A void element must have a tag.")
        else:
            tag = HTMLTags(self.tag)
            return self._to_html_helper(tag, "", self.props)
