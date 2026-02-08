from textnode import *

# node = TextNode("This is text with a `code block` word", TextType.TEXT)
# new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

# [
#     TextNode("This is text with a ", TextType.TEXT),
#     TextNode("code block", TextType.CODE),
#     TextNode(" word", TextType.TEXT),
# ]

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
                if i % 2 == 0:
                    if parts[i] == "":
                        continue
                    new_nodes.append(TextNode(parts[i], node.text_type))
                else:
                    new_nodes.append(TextNode(parts[i], text_type))
    return new_nodes