import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        sections = old_node.text.split(delimiter)
        if (len(sections) % 2) == 0:
            raise Exception("Invalid Markdown syntax")
        
        split_nodes = []
        for i in range(len(sections)):
            if sections[i] == "":
                continue 

            if (i % 2) == 1:
                split_nodes.append(TextNode(sections[i], text_type))
            else:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
        
        new_nodes.extend(split_nodes)
    
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str,str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text: str) -> list[tuple[str,str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

        
