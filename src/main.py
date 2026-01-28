from generate_page import generate_page
from get_static import get_static_assets


def main():
    static = "static"
    public = "public"
    get_static_assets(static, public)

    md = "content/index.md"
    template = "template.html"

    generate_page(md, template, public)


if __name__ == "__main__":
    main()
