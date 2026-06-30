import unittest
from blocknode import BlockType, markdown_to_blocks, block_to_block_type, markdown_to_html_node, extract_title, extract_title


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
            BlockType.ULIST
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
            BlockType.OLIST
        )

    def test_block_to_block_type_ordered_list_invalid_start(self):
        md = "2. item1\n3. item2"
        block = block_to_block_type(md)
        self.assertEqual(block, BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_list_non_sequential(self):
        md = "1. item1\n3. item2\n5. item3"
        block = block_to_block_type(md)
        self.assertEqual(block, BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        md = """
# Heading 1

## Heading 2

### Heading 3
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3></div>",
        )

    def test_blockquote(self):
        md = """
> This is a **quote** block
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a <b>quote</b> block</blockquote></div>",
        )


    def test_unordered_list(self):
        md = """
- item one
- item **two**
- item three
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>item one</li><li>item <b>two</b></li><li>item three</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. first
2. second
3. _third_
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>first</li><li>second</li><li><i>third</i></li></ol></div>",
        )

    def test_extract_title(self):
        md = "# Tolkien Fan Club"
        text = extract_title(md)
        self.assertEqual(
            text,
            "Tolkien Fan Club"
        )

    def test_extract_title_no_header(self):
        md = "Tolkien Fan Club"
        with self.assertRaises(Exception):
            extract_title(md)

    def test_extract_title(self):
        md = "# Hello World"
        self.assertEqual(extract_title(md), "Hello World")

    def test_extract_title_strips_whitespace(self):
        md = "#    Hello World    "
        self.assertEqual(extract_title(md), "Hello World")

    def test_extract_title_ignores_h2(self):
        md = "## Not H1\n# Real Title"
        self.assertEqual(extract_title(md), "Real Title")

    def test_extract_title_no_h1_raises(self):
        md = "## Only H2\nSome text"
        with self.assertRaises(Exception):
            extract_title(md)

if __name__ == "__main__":
    unittest.main()   