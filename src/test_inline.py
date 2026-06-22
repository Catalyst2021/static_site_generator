import unittest
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType

class TestSplitNodes(unittest.TestCase):
    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_list = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            ] 
        
        self.assertEqual(new_list, expected)
        
    def test_split_italics(self):
        node = TextNode("This is text with a _italic_ word", TextType.TEXT)
        new_list = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
            ] 
        
        self.assertEqual(new_list, expected)

    def test_split_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_list = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
            ] 
        
        self.assertEqual(new_list, expected)

    def test_non_text_node(self):
        node = TextNode("This is text with a **bold** word", TextType.BOLD)
        new_list = split_nodes_delimiter([node], "**", TextType.BOLD)

        expected = [TextNode("This is text with a **bold** word", TextType.BOLD, None)] 
        
        self.assertEqual(new_list, expected)

    def test_raises_on_unclosed(self):
        node = TextNode("This is text with a **bold word", TextType.TEXT) 

        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_delimiter_at_start(self):
        node = TextNode("**Bold** is at the start of text", TextType.TEXT)
        new_list = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [TextNode("Bold", TextType.BOLD),
                    TextNode(" is at the start of text", TextType.TEXT)]
        
        self.assertEqual(new_list, expected)
    
    def test_delimiter_at_end(self):
        node = TextNode("Bold is at the end of text **Bold**", TextType.TEXT)
        new_list = split_nodes_delimiter([node], "**", TextType.BOLD)

        expected = [TextNode("Bold is at the end of text ", TextType.TEXT),
                    TextNode("Bold", TextType.BOLD)]
        
        self.assertEqual(new_list, expected)
    
    def test_multiple_delimiters(self):
        node = TextNode("word **one** **two** **three** done", TextType.TEXT)
        new_list = split_nodes_delimiter([node], "**", TextType.BOLD)

        expected = [TextNode("word ", TextType.TEXT),
                    TextNode("one", TextType.BOLD),
                    TextNode(" ", TextType.TEXT),
                    TextNode("two", TextType.BOLD),
                    TextNode(" ", TextType.TEXT),
                    TextNode("three", TextType.BOLD),
                    TextNode(" done", TextType.TEXT)]
        
        self.assertEqual(new_list, expected)

    def test_empty_list(self):
        new_list = split_nodes_delimiter([], "**", TextType.BOLD)
        expected = []
        self.assertEqual(new_list, expected)


    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

if __name__ == "__main__":
    unittest.main()