import re
from textnode import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            parts = node.text.split(delimiter)
            if len(parts) % 2 == 0:
                raise Exception("Error: delimiter not closed")
            for i in range(len(parts)):
                if parts[i] == "":
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(parts[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(parts[i], text_type))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        matches = extract_markdown_images(text)

        if not matches:
            new_nodes.append(node)
            continue

        for alt, url in matches:
            markdown = f"![{alt}]({url})"
            parts = text.split(markdown, 1)

            if len(parts) != 2:
                raise ValueError(f"Invalid markdown image format: {markdown}")

            before, after = parts

            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))

            new_nodes.append(TextNode(alt, TextType.IMAGE, url))

            text = after

        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        matches = extract_markdown_links(text)

        if not matches:
            new_nodes.append(node)
            continue

        for anchor, url in matches:
            markdown = f"[{anchor}]({url})"
            parts = text.split(markdown, 1)

            if len(parts) != 2:
                raise ValueError(f"Invalid markdown link format: {markdown}")

            before, after = parts

            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))

            new_nodes.append(TextNode(anchor, TextType.LINK, url))

            text = after

        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    # Start with single TEXT node containing full input
    nodes = [TextNode(text, TextType.TEXT)]

    # Code: `code` -> pairs of `
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    
    # Order matters: simple delimiters first, then images/links
    # Bold: **text** -> pairs of **
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    
    # Italic: _italic_ -> pairs of _
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    
    # Images: ![alt](url)
    nodes = split_nodes_image(nodes)
    
    # Links: [text](url) - note negative lookbehind in regex to exclude images
    nodes = split_nodes_link(nodes)
    
    return nodes