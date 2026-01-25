import src.markdown_to_textnode as md2tn
from src.html_leafnode import LeafNode
from src.html_parentnode import ParentNode
from src.html_tags import HTMLTags as t
from src.htmlnode import HTMLNode
from src.markdown_to_blocks import BlockType
from src.markdown_to_blocks import block_to_block_type as b2bt
from src.markdown_to_blocks import markdown_to_blocks as md2b
from src.textnode import TextNode, TextType


def markdown_to_html(markdown: str) -> HTMLNode:
    blocks: list[str] = md2b(markdown)
    typed_blocks = {block: b2bt(block) for block in blocks}

    for block, block_type in typed_blocks.items():
        # parent nodes must be passed a list of HTMLNodes as children,
        # so we have to find and conver the children before rendering the blocks as HTMLModes

        match block_type:
            case BlockType.PARAGRAPH:
                # may contain inline text nodes
                pass
            case BlockType.HEADING:
                # may contain inline text nodes
                pass
            case BlockType.CODE:
                return code_block_to_html(block)
            case BlockType.QUOTE:
                # surrounded by <blockquote>
                pass
            case BlockType.UNDORDERED_LIST:
                # wrap it in a <ul>
                # children are <li>
                # <li> may contain child nodes
                pass
            case BlockType.ORDERED_LIST:
                # wrap it in a <ol>
                # children are <li>
                pass
            case _:
                raise ValueError("invalid block type detected")

    result = HTMLNode()
    return result


def code_block_to_html(text: str):
    children = [LeafNode(t.CODE.value, text, None)]
    return ParentNode(t.PRE.value, children, None)


def blockquote_to_html(text: str):
    if not isinstance(text, str):
        raise TypeError
    return ParentNode(t.BLOCKQUOTE.value, text_to_children(text), None)


def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = md2tn.text_to_textnodes(text)
    html_nodes: list[HTMLNode] = []
    for node in text_nodes:
        html_nodes.append(TextNode.text_node_to_html_node(node))
    return html_nodes
