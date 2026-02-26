#!/usr/bin/env python3

import re 
from enum import Enum
from inline_markdown import *
from htmlnode import *
from textnode import *

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

def text_to_children(text):
    child_nodes = []
    textnodes = text_to_textnodes(text)
    for node in textnodes:
        leafnode = text_node_to_html_node(node)
        child_nodes.append(leafnode)
    
    return child_nodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            block_clean = block.replace('\n', ' ')
            block_nodes.append(ParentNode("p", text_to_children(block_clean)))
        
        elif block_type == BlockType.HEADING:
            parts = block.split(" ", 1)
            block_nodes.append(ParentNode(f"h{len(parts[0])}", text_to_children(parts[1])))

        elif block_type == BlockType.CODE:
            block_clean = block[4:-3]
            textnode = TextNode(block_clean, TextType.CODE)
            block_nodes.append(ParentNode("pre", [text_node_to_html_node(textnode)]))

        elif block_type == BlockType.QUOTE:
            lines = block.split("\n")
            text = " ".join(line.lstrip("> ") for line in lines)
            block_nodes.append(ParentNode("blockquote", text_to_children(text)))
        
        elif block_type == BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            child_nodes = []
            for line in lines:
                child_nodes.append(ParentNode("li", text_to_children(line[2:])))
            block_nodes.append(ParentNode("ul", child_nodes))

        elif block_type == BlockType.ORDERED_LIST:
            lines = block.split("\n")
            child_nodes = []
            for line in lines:
                line_clean = line.split(". ", 1)
                child_nodes.append(ParentNode("li", text_to_children(line_clean[1])))
            block_nodes.append(ParentNode("ol", child_nodes))
        
        else:
            raise ValueError(f"Unknown block type: {block_type}")

    return ParentNode("div", block_nodes)
