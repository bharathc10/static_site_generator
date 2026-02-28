import os
from markdown_blocks import *

def extract_title(markdown):
    lines = markdown.split('\n')
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    
    raise Exception("No h1 heading")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with (
        open(from_path, 'r', encoding='utf-8') as f_md,
        open(template_path, 'r', encoding='utf-8') as f_temp
    ):
        markdown_content = f_md.read()
        template_content = f_temp.read()

    html = markdown_to_html_node(markdown_content).to_html()
    template_content = template_content.replace("{{ Title }}", extract_title(markdown_content))
    template_content = template_content.replace("{{ Content }}", html)

    dir_path = os.path.dirname(dest_path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)

    with open(dest_path, 'w', encoding='utf-8') as f_dest:
        f_dest.write(template_content)
        