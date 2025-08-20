import re
from enum import Enum 

BlockType = Enum("paragraph", "heading", "code", "quote", "unordered_list", "ordered_list")
class BlockType(Enum):
    PARAGRAPH= "paragraph"
    HEADING = "heading"
    CODE = "code" 
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown:str):
    splits = markdown.split("\n\n")

    final_blocks = []

    for split in splits:
        if split == "":
            continue
        final_blocks.append(split.strip())
    
    return final_blocks

def bock_to_block_type(block:str):
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
