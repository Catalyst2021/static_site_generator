import unittest
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
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

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_links(self):
        node = TextNode(
             "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_images_no_images(self):
        node = TextNode("Just plain text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_images_image_at_start(self):
        node = TextNode("![cat](cat.png) some text after", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("cat", TextType.IMAGE, "cat.png"),
                TextNode(" some text after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_image_at_end(self):
        node = TextNode("some text before ![cat](cat.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("some text before ", TextType.TEXT),
                TextNode("cat", TextType.IMAGE, "cat.png"),
            ],
            new_nodes,
        )

    def test_split_images_non_text_node_unchanged(self):
        node = TextNode("bold text", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links_no_links(self):
        node = TextNode("Just plain text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links_link_at_start(self):
        node = TextNode("[boot dev](https://www.boot.dev) is great", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" is great", TextType.TEXT),
            ],
            new_nodes,
        )
        
    def test_split_images_multiple_nodes(self):
        nodes = [
            TextNode("![cat](cat.png)", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("text ![dog](dog.png) end", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("cat", TextType.IMAGE, "cat.png"),
                TextNode("bold", TextType.BOLD),
                TextNode("text ", TextType.TEXT),
                TextNode("dog", TextType.IMAGE, "dog.png"),
                TextNode(" end", TextType.TEXT),
            ],
            new_nodes,
        )
    

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_plain_text(self):
        nodes = text_to_textnodes("Just plain text")
        self.assertListEqual(
            [TextNode("Just plain text", TextType.TEXT)],
            nodes,
        )

    def test_bold_only(self):
        nodes = text_to_textnodes("**bold**")
        self.assertListEqual(
            [TextNode("bold", TextType.BOLD)],
            nodes,
        )

    def test_multiple_bold(self):
        nodes = text_to_textnodes("**one** and **two**")
        self.assertListEqual(
            [
                TextNode("one", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("two", TextType.BOLD),
            ],
            nodes,
        )

    def test_invalid_bold(self):
        with self.assertRaises(Exception):
            text_to_textnodes("**unclosed bold")

    def test_empty_string(self):
        nodes = text_to_textnodes("")
        self.assertListEqual([], nodes)

if __name__ == "__main__":
    unittest.main()   
