import os
import shutil


def _reset_public(public):
    shutil.rmtree(public)
    os.mkdir(public)


def get_static_assets(static_dir: str, public_dir: str) -> None:
    if not (isinstance(static_dir, str) and isinstance(public_dir, str)):
        raise TypeError

    if not (os.path.exists(static_dir) and os.path.exists(public_dir)):
        raise ValueError

    if not (os.path.isdir(static_dir) and os.path.isdir(public_dir)):
        raise NotADirectoryError

    visited: set = set()
    static: str = os.path.abspath(static_dir)
    public: str = os.path.abspath(public_dir)
    _reset_public(public)
    dfs_visit(public, static, visited)


def dfs_visit(public, node, visited):
    stack: list[str] = []
    visited.add(node)
    files = os.listdir(node)
    for file in files:
        file_path = os.path.join(node, file)
        if not os.path.isfile(file_path):
            stack.append(file)
        else:
            shutil.copy(file_path, public)

    while len(stack) > 0:
        dir = stack.pop()
        pub = os.path.join(public, dir)
        if not os.path.exists(pub):
                os.mkdir(pub)
        stat = os.path.join(node, dir)
        dfs_visit(pub, stat, visited)


if __name__ == "__main__":
    static = "static"
    public = "public"
    get_static_assets(static, public)
