import os 
import shutil
import sys

from gencontent import generate_page

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


def generate_pages_recursive(content_dir: str, template_source: str, basepath: str):

    for dirpath, dirnames, filenames in os.walk(content_dir):
        for filename in filenames:
            if filename.endswith(".md"):
                from_path = os.path.join(dirpath, filename)
                rel_path = os.path.relpath(dirpath, content_dir)
                dest_path = os.path.join("public", rel_path, filename.replace(".md", ".html"))
                generate_page(from_path, template_source, dest_path, basepath)

def main():
    copy_static("static", "docs")
    #content_dir = "content"
    template_source = "template.html"


    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    generate_pages_recursive(basepath, template_source, basepath)



if __name__ == "__main__":
    main()