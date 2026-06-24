from enum import Enum
import re

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
        if all(line.startwith("- ") for line in lines):
            return BlockType.ULIST
   
    if block.startswith("1. "):
        if all(line.startwith(f"{i}. ") for i, line in enumerate(lines, 1)):
            return BlockType.OLIST
 
    return BlockType.PARAGRAPH

