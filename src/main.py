import os 
import shutil

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



def main():
    copy_static("static", "public")
    markdown_source = "content/index.md"
    template_source = "template.html"
    html_destination = "public/index.html"
    generate_page(markdown_source, template_source, html_destination)


if __name__ == "__main__":
    main()