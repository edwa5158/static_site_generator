import os
from sys import argv
from typing import Optional

from get_static import get_static_assets
from markdown_to_html import markdown_to_html
from parse_markdown import extract_title


def generate_page(
    from_md_file: str,
    html_template_file: str,
    html_dest_dir: str,
    basepath: str,
):
    # print(
    #     f"Generating page from {from_md_file} to {html_dest_dir} using {html_template_file}"
    # )

    md_full_path: str = os.path.abspath(from_md_file)
    template_full_path: str = os.path.abspath(html_template_file)
    html_dest_full_path: str = os.path.abspath(html_dest_dir)

    with open(md_full_path) as f:
        md = f.read()

    with open(template_full_path) as f:
        template = f.read()

    html_nodes = markdown_to_html(md)
    html_content = html_nodes.to_html()
    title = extract_title(md)
    html = template.replace("{{ Title }}", title)
    html = html.replace("{{ Content }}", html_content)
    html = html.replace('href="/', f'href="{basepath}')
    html = html.replace('src="/', f"{basepath}")

    # if not os.path.exists(dest_full_path):
    os.makedirs(html_dest_full_path, exist_ok=True)

    dest_full_path = os.path.join(html_dest_full_path, "index.html")

    with open(dest_full_path, "w") as f:
        f.write(html)


def generate_pages_recursive(
    from_md_dir: str,
    html_template_file: str,
    html_dest_dir: str,
    basepath: str,
) -> None:
    if not (
        isinstance(from_md_dir, str)
        and isinstance(html_template_file, str)
        and isinstance(html_dest_dir, str)
    ):
        raise TypeError("the provided paths must be strings")

    os.makedirs(from_md_dir, exist_ok=True)
    os.makedirs(html_dest_dir, exist_ok=True)

    if not (os.path.isdir(from_md_dir) and os.path.isdir(html_dest_dir)):
        raise ValueError("one of the supplied paths does not exist")

    visited: set = set()
    md_content_dir: str = os.path.abspath(from_md_dir)
    html_template_file: str = os.path.abspath(html_template_file)
    html_output_directory: str = os.path.abspath(html_dest_dir)
    dfs_visit(
        md_content_dir, html_template_file, html_output_directory, visited, basepath
    )


def dfs_visit(
    current_source_dir: str,
    template_path: str,
    dest_dir: str,
    visited: set,
    basepath: str,
):
    stack: list[str] = []
    visited.add(current_source_dir)

    # Copy all the files in current_source_dir to dest_dir
    for fso_name in os.listdir(current_source_dir):
        item_path = os.path.join(current_source_dir, fso_name)
        if os.path.isfile(item_path):
            # item_path is a file, so make an html page in the destimation
            if os.path.splitext(item_path)[1] == ".md":
                generate_page(item_path, template_path, dest_dir, basepath)
        else:
            # item path is a dir, so put it on the stack and create the dest dir
            stack.append(item_path)
            os.makedirs(os.path.join(dest_dir, fso_name), exist_ok=True)

    while len(stack) > 0:
        next_source_dir = stack.pop()
        dir_name = os.path.basename(next_source_dir)
        new_dest_dir = os.path.join(dest_dir, dir_name)
        next_source_dir_path = os.path.join(current_source_dir, next_source_dir)
        dfs_visit(next_source_dir_path, template_path, new_dest_dir, visited, basepath)


def main():
    # content = "static"
    # template = "template.html"
    # dest = "public"
    # basepath =
    # generate_pages_recursive(content, template, dest, basepath)

    basepath: str = argv[0] or "\\"

    static = "static"
    public = "docs"
    get_static_assets(static, public)

    generate_pages_recursive("content", "template.html", public, basepath)


if __name__ == "__main__":
    main()
