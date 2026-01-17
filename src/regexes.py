import re


def extract_markdown_images(text: str) -> list[tuple[str, str, str]]:
    # pat = r"!\[(.*?)\]\((.*?)\)"
    pat = r"(?P<image>!\[(?P<alt_text>.*?)\]\((?P<url>.*?)\))"
    matches = re.finditer(pat, text)
    results: list[tuple[str, str, str]] = []
    for match in matches:
        result = (match.group("alt_text"), match.group("url"), match.group("image"))
        results.append(result)
    return results


def extract_markdown_links(text: str) -> list[tuple[str, str, str]]:
    # pat = r"(?<!pattern)\[(.*?)\]\((.*?)\)"
    pat = r"(?<!\!)(?P<link>\[(?P<alt_text>.*?)\]\((?P<url>.*?)\))"
    matches = re.finditer(pat, text)
    results: list[tuple[str, str, str]] = []
    for match in matches:
        result = (match.group("alt_text"), match.group("url"), match.group("link"))
        results.append(result)
    return results
