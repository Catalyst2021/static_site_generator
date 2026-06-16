from textnode import TextType, TextNode
from htmlnode import HTMLNode

def main():
    text = "This is some anchor text"
    text_type = "link"
    url = "https://www.boot.dev"

    print(TextNode(text, text_type, url))

if __name__ == "__main__":
    main()