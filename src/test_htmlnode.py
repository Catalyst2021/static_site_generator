import unittest
from htmlnode import HTMLNode

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

       

if __name__ == "__main__":
    unittest.main()