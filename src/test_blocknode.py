import unittest
from blocknode import BlockType, markdown_to_blocks, block_to_block_type


class TestBlockNodes(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = "Block one\n\n\n\nBlock two"
        blocks = markdown_to_blocks(md)
        
        self.assertEqual(
            blocks,
            [
                "Block one",
                "Block two",
            ]

        )
    
    def test_markdown_to_blocks_whitespace(self):
        md = "\n\nBlock one\n\nBlock two\n\n"
        blocks = markdown_to_blocks(md)
        
        self.assertEqual(
            blocks,
            [
                "Block one",
                "Block two",
            ]

        )

    def test_markdown_to_blocks_leading_spaces(self):
        md = "  Block one  \n\n  Block two  "
        blocks = markdown_to_blocks(md)
        
        self.assertEqual(
            blocks,
            [
                "Block one",
                "Block two",
            ]

        )

    def test_markdown_to_blocks_no_newlines(self):
        md  = "Just one block"
        blocks = markdown_to_blocks(md)
        
        self.assertEqual(
            blocks,
            [
                "Just one block"
            ]

        )

    def test_markdown_to_blocks_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        
        self.assertEqual(
            blocks,
            []
        )

    def test_block_to_block_type_paragraph(self):
        md = "test text"
        block = block_to_block_type(md)

        self.assertEqual(
            block,
            BlockType.PARAGRAPH
        )



    def test_block_to_block_type_heading(self):
        md = "###### Heading"
        block = block_to_block_type(md)

        self.assertEqual(
            block,
            BlockType.HEADING
        )

    def test_block_to_block_type_heading_invalid(self):
        md = "####### Too many hashes"
        block = block_to_block_type(md)
        self.assertEqual(block, BlockType.PARAGRAPH)

    def test_block_to_block_type_heading_invalid(self):
        md = "####### Too many hashes"
        block = block_to_block_type(md)
        self.assertEqual(block, BlockType.PARAGRAPH)

    

    def test_block_to_block_type_code(self):
        md = """```
for i in range(6):
    print(i)
```
"""
        block = block_to_block_type(md.strip())

        self.assertEqual(
            block,
            BlockType.CODE
        )

    def test_block_to_block_type_quote(self):
        md = ">Famous quote\n>more famous quote"
        block = block_to_block_type(md)

        self.assertEqual(
            block,
            BlockType.QUOTE
        )

    def test_block_to_block_type_quote_invalid(self):
        md = ">Famous quote\nno arrow here"
        block = block_to_block_type(md)
        self.assertEqual(block, BlockType.PARAGRAPH)

    def test_block_to_block_type_unordered_list(self):
        md = "- item1\n- item2\n- item3"
        block = block_to_block_type(md)

        self.assertEqual(
            block,
            BlockType.UNORDERED_LIST
        )
        
    def test_block_to_block_type_unordered_list_invalid(self):
        md = "- item1\nitem2\n- item3"
        block = block_to_block_type(md)
        self.assertEqual(block, BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_list(self):
        md = "1. item1\n2. item2\n3. item3"
        block = block_to_block_type(md)

        self.assertEqual(
            block,
            BlockType.ORDERED_LIST
        )

    def test_block_to_block_type_ordered_list_invalid_start(self):
        md = "2. item1\n3. item2"
        block = block_to_block_type(md)
        self.assertEqual(block, BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_list_non_sequential(self):
        md = "1. item1\n3. item2\n5. item3"
        block = block_to_block_type(md)
        self.assertEqual(block, BlockType.PARAGRAPH)

    
if __name__ == "__main__":
    unittest.main()   