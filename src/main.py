import os 
import shutil


from textnode import TextType, TextNode
from htmlnode import HTMLNode

def copy_static(src, dst):

    if os.path.exists(dst):
        shutil.rmtree(dst)
    
    os.mkdir(dst)

    for item in os.listdir(src):
        if os.path.isfile(os.path.join(src, item)):
            shutil.copy(os.path.join(src, item), os.path.join(dst, item))
            print(f"Copying {os.path.join(src, item)} to {os.path.join(dst, item)}")
        else:
            copy_static(os.path.join(src,item), os.path.join(dst, item))



def main():
    text = "This is some anchor text"
    text_type = "link"
    url = "https://www.boot.dev"

    print(TextNode(text, text_type, url))

    copy_static("static", "public")


if __name__ == "__main__":
    main()