from src.markdown_to_textnode import Delimiter, delimiter_doesnt_match
from src.textnode import TextNode, TextType


def main():
    print(delimiter_doesnt_match(TextType.BOLD, Delimiter.CODE.value))


if __name__ == "__main__":
    main()
