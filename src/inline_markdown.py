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

        
def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            new_nodes.append(old_node)
            continue
             
        markdown_images_tuple = extract_markdown_images(old_node.text)
        if not markdown_images_tuple:
            new_nodes.append(old_node)
            continue

        remaining_text = old_node.text
        for i in markdown_images_tuple:
            image_alt, image_link = i[0], i[1]

            sections = remaining_text.split(f"![{image_alt}]({image_link})", 1)
            
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            remaining_text = sections[1]
    
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes
        


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:

    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            new_nodes.append(old_node)
            continue
             
        markdown_images_tuple = extract_markdown_links(old_node.text)
        if not markdown_images_tuple:
            new_nodes.append(old_node)
            continue

        remaining_text = old_node.text
        for i in markdown_images_tuple:
            url_alt, url_link = i[0], i[1]

            sections = remaining_text.split(f"[{url_alt}]({url_link})", 1)
            
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            new_nodes.append(TextNode(url_alt, TextType.LINK, url_link))
            remaining_text = sections[1]
    
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes   

def text_to_textnodes(text: str) -> list[TextNode]:

    nodes = split_nodes_delimiter([TextNode(text,TextType.TEXT)], "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes