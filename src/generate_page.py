import os

from markdown_to_html import markdown_to_html
from parse_markdown import extract_title


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    md__full_path: str = os.path.abspath(from_path)
    template_full_path: str = os.path.abspath(template_path)
    dest_full_path: str = os.path.abspath(dest_path)

    with open(md__full_path) as f:
        md = f.read()

    with open(template_full_path) as f:
        template = f.read()

    html_content = markdown_to_html(md).to_html()
    title = extract_title(md)
    html = template.replace("{{ Title }}", title)
    html = html.replace("{{ Content }}", html_content)

    if not os.path.exists(dest_full_path):
        os.makedirs(dest_full_path)

    dest_full_path = os.path.join(dest_full_path, "index.html")

    with open(dest_full_path, "w") as f:
        f.write(html)
