def markdown_to_blocks(markdown: str) -> list[str]:
    if not type(markdown) is str:
        raise TypeError(f"invalid input type {type(markdown)}; only strings accepted")
    
    initial_blocks: list[str] = markdown.split("\n\n")
    blocks: list[str] = []
    for block in initial_blocks:
        block = block.strip()
        if len(block) > 0:
            blocks.append(block)
    return blocks
