from typing import Optional

import markdown_to_textnode as md2tn
from html_leafnode import LeafNode
from html_parentnode import ParentNode
from html_tags import HTMLTags
from htmlnode import HTMLNode
from parse_markdown import BlockType
from parse_markdown import block_to_block_type as b2bt
from parse_markdown import extract_title
from parse_markdown import markdown_to_blocks as md2b
from textnode import TextNode, TextType


def markdown_to_html(markdown: str) -> HTMLNode:
    if not isinstance(markdown, str):
        raise TypeError

    blocks: list[str] = md2b(markdown)
    typed_blocks = {block: b2bt(block) for block in blocks}
    children: list[HTMLNode] = []
    child: HTMLNode

    for block, block_type in typed_blocks.items():
        # parent nodes must be passed a list of HTMLNodes as children,
        # so we have to find and conver the children before rendering the blocks as HTMLModes

        match block_type:
            case BlockType.PARAGRAPH:
                child = md_to_paragraph(block)
            case BlockType.HEADING:
                child = md_to_heading(block)
            case BlockType.CODE:
                child = code_block_to_html(block)
            case BlockType.QUOTE:
                child = blockquote_to_html(block)
            case BlockType.UNDORDERED_LIST:
                child = md_to_unordered_list(block)
            case BlockType.ORDERED_LIST:
                child = md_to_ordered_list(block)
            case _:
                raise ValueError("invalid block type detected")
        children.append(ParentNode(HTMLTags.DIV.value, [child]))

    body = ParentNode(HTMLTags.BODY.value, children)
    return ParentNode(HTMLTags.HTML.value, [body])


def md_to_paragraph(md: str) -> HTMLNode:
    if not isinstance(md, str):
        raise TypeError

    children = text_to_children(md)
    return ParentNode(HTMLTags.PARAGRAPH.value, children)


def md_to_heading(md: str) -> HTMLNode:
    if not isinstance(md, str):
        raise TypeError

    def map_heading(text: str) -> HTMLTags:
        count = len(text) - len(text.lstrip("#"))
        match count:
            case 1:
                return HTMLTags.H1
            case 2:
                return HTMLTags.H2
            case 3:
                return HTMLTags.H3
            case 4:
                return HTMLTags.H4
            case 5:
                return HTMLTags.H5
            case 6:
                return HTMLTags.H6
            case _:
                raise ValueError

    if map_heading(md) == HTMLTags.H1:
        children = text_to_children(extract_title(md))
    else:
        children = text_to_children(md.lstrip("#").lstrip())

    return ParentNode(map_heading(md).value, children)


def md_to_unordered_list(md: str) -> HTMLNode:
    if not isinstance(md, str):
        raise TypeError
    children = _list_items_to_html(md)
    return ParentNode(HTMLTags.UNORDERED_LIST.value, children)


def md_to_ordered_list(md: str) -> HTMLNode:
    if not isinstance(md, str):
        raise TypeError
    children = _list_items_to_html(md, True)
    return ParentNode(HTMLTags.ORDERED_LIST.value, children)


def _list_items_to_html(md: str, ordered: Optional[bool] = False) -> list[ParentNode]:
    if not isinstance(md, str):
        raise TypeError

    lines = md.split("\n")
    result: list[ParentNode] = []
    for line in lines:
        if ordered:
            line = line.split(". ", 1)[1]
        else:
            line = line.split("- ", 1)[1]

        children: list[HTMLNode] = text_to_children(line)
        parent: ParentNode = ParentNode(HTMLTags.LIST_ITEM.value, children)
        result.append(parent)
    return result


def code_block_to_html(text: str):
    children = [LeafNode(HTMLTags.CODE.value, text, None)]
    return ParentNode(HTMLTags.PRE.value, children, None)


def blockquote_to_html(text: str):
    if not isinstance(text, str):
        raise TypeError
    lines = text.split("\n")
    for i in range(len(lines)):
        lines[i] = lines[i][1:].lstrip()
    lines = "\n".join(lines)
    return ParentNode(HTMLTags.BLOCKQUOTE.value, text_to_children(lines), None)


def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = md2tn.text_to_textnodes(text)
    html_nodes: list[HTMLNode] = []
    for node in text_nodes:
        html_nodes.append(TextNode.text_node_to_html_node(node))
    return html_nodes
