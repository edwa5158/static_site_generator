import re


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    pat = r"!\[(.*?)\]\((.*?)\)"
    return re.findall(pat,text)