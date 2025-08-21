import re
from enum import Enum 
from htmlnode import ParentNode
from inline_markdown import text_to_text_nodes
from textnode import text_node_to_html_node, TextNode, TextType

BlockType = Enum("paragraph", "heading", "code", "quote", "unordered_list", "ordered_list")
class BlockType(Enum):
    PARAGRAPH= "paragraph"
    HEADING = "heading"
    CODE = "code" 
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown:str) -> list[str]:
    splits = markdown.split("\n\n")

    final_blocks = []

    for split in splits:
        if split == "":
            continue
        final_blocks.append(split.strip())
    
    return final_blocks

def block_to_block_type(block:str):
    lines = block.split("\n")
    # heading
    if re.match(r"^#{1,6} .+", block):
        return BlockType.HEADING

    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    if block.startswith(">"):
        return BlockType.QUOTE
    
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    # ordered list
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        node = block_to_html_node(block)
        children.append(node)
    
    return ParentNode("div", children, None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)

    if block_type == BlockType.PARAGRAPH:
       return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    
    raise ValueError("Invalid block type")


def text_to_children(text):
    nodes = text_to_text_nodes(text)
    children = []
    for node in nodes:
        html_node = text_node_to_html_node(node)
        children.append(html_node)
    
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    
    if level + 1 >= len(block):
        raise ValueError(f"Invalid header level: {level}")
    
    text = block[level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block:str):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def ordered_list_to_html_node(block:str):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item.split(". ", maxsplit=1)[1]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def unordered_list_to_html_node(block:str):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def extract_markdown_title(markdown:str):
    blocks = markdown_to_blocks(markdown)

    header = None
    for block in blocks:
        if block_to_block_type(block) == BlockType.HEADING:
            if block.startswith("# "):
                header = block
                break
    
    if header is None:
        raise Exception("no header found")
    
    return header.strip("# ")
