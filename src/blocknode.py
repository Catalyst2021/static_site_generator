from enum import Enum
from htmlnode import HTMLNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def markdown_to_blocks(markdown: str) -> list[str]:
    new_blocks = []

    for block in markdown.split("\n\n"):
        if block:
            new_blocks.append(block.strip())

    return new_blocks

def block_to_block_type(block:str) -> BlockType:
    lines = block.split("\n")

    if block.startswith(("# ", "## ","### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
        
    if block.startswith("```\n"):
        if lines[-1] == "```":
            return BlockType.CODE
  
    if block.startswith(">"):
        if all(line.startswith(">") for line in lines):
            return BlockType.QUOTE

    if block.startswith("- "):
        if all(line.startswith("- ") for line in lines):
            return BlockType.ULIST
   
    if block.startswith("1. "):
        if all(line.startswith(f"{i}. ") for i, line in enumerate(lines, 1)):
            return BlockType.OLIST
 
    return BlockType.PARAGRAPH

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))

    return html_nodes
    

def markdown_to_html_node(markdown: str) -> str:
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            text = " ".join(block.split("\n"))
            children = text_to_children(text)
            node = ParentNode("p", children)
            block_nodes.append(node)

        elif block_type == BlockType.QUOTE:
            lines = block.split("\n")
            stripped = " ".join(line.lstrip(">").strip() for line in lines)
            children = text_to_children(stripped)
            node = ParentNode("blockquote", children)
            block_nodes.append(node)

        elif block_type == BlockType.CODE:
            text = block[4:-3]
            text_node = TextNode(text, TextType.TEXT)
            children = text_node_to_html_node(text_node)
            node = ParentNode("pre", [ParentNode("code", [children])])
            block_nodes.append(node)

        elif block_type == BlockType.ULIST:
            items = []

            for line in block.split("\n"):
                text = line[2:]
                children = text_to_children(text)
                items.append(ParentNode("li", children))
            node = ParentNode("ul", items)
            block_nodes.append(node)

        elif block_type == BlockType.OLIST:
            items = []

            for line in block.split("\n"):
                text = line.split(". ", 1)[1]
                children = text_to_children(text)
                items.append(ParentNode("li", children))
            node = ParentNode("ol", items)
            block_nodes.append(node)

        elif block_type == BlockType.HEADING:
            level = len(block) - len(block.lstrip("#"))
            text = block[level + 1 :]
            children = text_to_children(text)
            node = ParentNode(f"h{level}", children)
            block_nodes.append(node)

  

        
    return ParentNode("div", block_nodes)
        

  
        

