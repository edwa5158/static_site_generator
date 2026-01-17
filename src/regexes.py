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


def is_heading(md: str) -> bool:
    pat = r"#{1,6} [\w\d\s]+"
    match = re.fullmatch(pat, md)
    return True if match else False


def is_code(md: str) -> bool:
    pat = r"```\n[\s\S]*```"
    match = re.fullmatch(pat, md)
    return True if match else False


def is_quote(md: str) -> bool:
    pat = r"<[\s\S]*>"
    match = re.fullmatch(pat, md)
    return True if match else False


def is_unordered_list(md: str) -> bool:
    pat = r"\A(?:(- .*)\n{0,1})*\n{0,1}"
    match = re.fullmatch(pat, md)
    return True if match else False


def is_ordered_list(md: str) -> bool:
    lines = md.split("\n")
    line_num = 1
    for line in lines:
        prefix = f"{line_num}. "
        if line[: len(prefix)] == prefix:
            line_num += 1
        else:
            return False
    return True
