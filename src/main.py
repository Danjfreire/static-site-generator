from textnode import TextNode, TextType
from file_util import copy_files
from markdown_blocks import markdown_to_html_node, extract_markdown_title
import os
import sys

def main():
    path = sys.argv[1]
    basepath = path if not None else "/"


    copy_files("static", "docs")
    generate_pages_recursevely("content", "template.html", "docs", basepath)


def generate_pages_recursevely(dir_path_content, template_path, dest_dir_path, basepath):
    if not os.path.exists(dir_path_content):
        raise Exception(f"Invalid directory : {dir_path_content}")
    
    files = os.listdir(dir_path_content)

    for filename in files:
        file_path = os.path.join(dir_path_content, filename)
        if os.path.isfile(file_path):
            dest_path = os.path.join(dest_dir_path, filename.replace(".md", ".html"))
            generate_page(file_path, template_path, dest_path, basepath)
        elif os.path.isdir(file_path):
            generate_pages_recursevely(file_path, template_path, os.path.join(dest_dir_path, filename), basepath)
        

def generate_page(from_path: str, template_path: str, dest_path: str, basepath:str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    if not os.path.exists(from_path):
        raise Exception(f"File not found : {from_path}")

    if not os.path.exists(template_path):
        raise Exception(f"File not found : {from_path}")
    
    with open(from_path, "r") as markdown_file:
        markdown_content = markdown_file.read()

    with open(template_path, "r") as html_file:
        template_content = html_file.read()
    
    html = markdown_to_html_node(markdown_content).to_html()
    title = extract_markdown_title(markdown_content)
    filled_template = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html)
    filled_template = filled_template.replace('href="/', f'href="{basepath}')
    filled_template = filled_template.replace('src="/', f'src="{basepath}')


    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir, exist_ok=True)
        print(f"Created directory: {dest_dir}")

    with open(dest_path, "w") as output:
        output.write(filled_template)
        

if __name__ == "__main__":
    main()
