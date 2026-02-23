#!/usr/bin/env python3

import re 
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    clean_blocks = [block.strip() for block in blocks if block.strip()]
    
    return clean_blocks

def block_to_block_type(block):
    lines = block.split("\n")

    if re.match(r"^#{1,6} ", lines[0]):
        return BlockType.HEADING
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    
    ordered = True
    for index, line in enumerate(lines, start=1):
        if not line.startswith(f"{index}. "):
            ordered = False
            break
    if ordered:
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH