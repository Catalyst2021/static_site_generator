import os 

from blocknode import markdown_to_html_node, extract_title

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as md_file:
        md_content = md_file.read()

    with open(template_path, "r") as t_file:
        t_content = t_file.read()

    node = markdown_to_html_node(md_content)
    html = node.to_html()
    title = extract_title(md_content)

    template = t_content.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    
    dest_dir = os.path.dirname(dest_path)
    if dest_dir != "":
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(template)
  
    