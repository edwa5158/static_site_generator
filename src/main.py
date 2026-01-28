from generate_page import generate_pages_recursive
from get_static import get_static_assets


def main():
    static = "static"
    public = "public"
    get_static_assets(static, public)

    generate_pages_recursive("content", "template.html", public)


if __name__ == "__main__":
    main()
