from __future__ import annotations

from enum import Enum


class HTMLTags(Enum):
    HTML = "html"
    BODY = "body"
    HEAD = "head"
    PARAGRAPH = "p"
    ANCHOR = "a"
    IMAGE = "img"
    UNORDERED_LIST = "ul"
    ORDERED_LIST = "ol"
    LIST_ITEM = "li"
    BOLD = "b"
    ITALICS = "i"
    SPAN = "span"
    DIV = "div"
    META = "meta"
    TITLE = "title"
    H1 = "h1"
    H2 = "h2"
    H3 = "h3"
    H4 = "h4"
    H5 = "h5"
    H6 = "h6"
    CODE = "code"

    def opening_tag(self) -> str:
        match self:
            case HTMLTags.HTML:
                return "<html>"
            case HTMLTags.BODY:
                return "<body>"
            case HTMLTags.HEAD:
                return "<head>"
            case HTMLTags.IMAGE:
                return "<img>"
            case HTMLTags.UNORDERED_LIST:
                return "<ul>"
            case HTMLTags.ORDERED_LIST:
                return "<ol>"
            case HTMLTags.LIST_ITEM:
                return "<li>"
            case HTMLTags.ANCHOR:
                return "<a>"
            case HTMLTags.PARAGRAPH:
                return "<p>"
            case HTMLTags.BOLD:
                return "<b>"
            case HTMLTags.ITALICS:
                return "<i>"
            case HTMLTags.SPAN:
                return "<span>"
            case HTMLTags.DIV:
                return "<div>"
            case HTMLTags.META:
                return "<meta>"
            case HTMLTags.TITLE:
                return "<title>"
            case HTMLTags.H1:
                return "<h1>"
            case HTMLTags.H2:
                return "<h2>"
            case HTMLTags.H3:
                return "<h3>"
            case HTMLTags.H4:
                return "<h4>"
            case HTMLTags.H5:
                return "<h5>"
            case HTMLTags.H6:
                return "<h6>"
            case HTMLTags.CODE:
                return "<code>"
            case _:
                raise ValueError("invalid tag type")

    def closing_tag(self) -> str:
        match self:
            case HTMLTags.HTML:
                return "</html>"
            case HTMLTags.BODY:
                return "</body>"
            case HTMLTags.HEAD:
                return "</head>"
            case HTMLTags.IMAGE:
                return "</img>"
            case HTMLTags.UNORDERED_LIST:
                return "</ul>"
            case HTMLTags.ORDERED_LIST:
                return "</ol>"
            case HTMLTags.LIST_ITEM:
                return "</li>"
            case HTMLTags.ANCHOR:
                return "</a>"
            case HTMLTags.PARAGRAPH:
                return "</p>"
            case HTMLTags.BOLD:
                return "</b>"
            case HTMLTags.ITALICS:
                return "</i>"
            case HTMLTags.SPAN:
                return "</span>"
            case HTMLTags.DIV:
                return "</div>"
            case HTMLTags.META:
                return ""
            case HTMLTags.TITLE:
                return "</title>"
            case HTMLTags.H1:
                return "</h1>"
            case HTMLTags.H2:
                return "</h2>"
            case HTMLTags.H3:
                return "</h3>"
            case HTMLTags.H4:
                return "</h4>"
            case HTMLTags.H5:
                return "</h5>"
            case HTMLTags.H6:
                return "</h6>"
            case HTMLTags.CODE:
                return "</code>"
            case _:
                raise ValueError("invalid tag type")
