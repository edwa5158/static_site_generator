from sys import argv

from generate_page import generate_pages_recursive
from get_static import get_static_assets


def main():
    basepath: str = argv[0] or "\\"

    static = "static"
    public = "public"
    get_static_assets(static, public)

    generate_pages_recursive("content", "template.html", public, basepath)


if __name__ == "__main__":
    main()
