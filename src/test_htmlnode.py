import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHtmlNode(unittest.TestCase):

    def test_props_to_html_output(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank",})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')
    
    def test_props_to_html_empty(self):
        node = HTMLNode(props="")
        self.assertEqual(node.props_to_html(), '')
    
    def test_prop_to_html_none(self):
        node = HTMLNode(props=None)
        self.assertEqual(node.props_to_html(), '')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(),"<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_multiple_children(self):
        child_node = LeafNode("span", "child1")
        child_node2 = LeafNode("h1", "child2")
        child_node3 = LeafNode("h2", "child3")
        parent_node = ParentNode("div", [child_node, child_node2, child_node3])
        self.assertEqual(parent_node.to_html(), "<div><span>child1</span><h1>child2</h1><h2>child3</h2></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_no_children(self):
        node = ParentNode("h1", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_nested_properties(self):
        leaf = LeafNode("a", "Click me", {"href": "https://www.google.com"})
        child = ParentNode("span", [leaf], {"class": "sub-text"})
        parent = ParentNode("div", [child], {"id": "main-container"})

        expected = '<div id="main-container"><span class="sub-text"><a href="https://www.google.com">Click me</a></span></div>'
        self.assertEqual(parent.to_html(), expected)
    
    def test_to_html_no_tag(self):
        node = ParentNode(None, [LeafNode("span", "child")])
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_to_html_mixed_children(self):
        leaf1 = LeafNode("b", "Bold")
        leaf2 = LeafNode(None, " plain text ")
        nested_parent = ParentNode("span", [LeafNode("i", "italic")])
        
        parent = ParentNode("p", [leaf1, leaf2, nested_parent])
        expected = "<p><b>Bold</b> plain text <span><i>italic</i></span></p>"
        self.assertEqual(parent.to_html(), expected)

if __name__ == "__main__":
    unittest.main()