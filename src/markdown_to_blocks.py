def markdown_to_blocks(markdowon: str) -> list[str]:
    initial_blocks: list[str] = markdowon.split("\n\n")
    blocks: list[str] = []
    for block in initial_blocks:
        block = block.strip()
        if len(block) > 0:
            blocks.append(block)
    return blocks

import unittest



