import os
import shutil


def _reset_public(public):
    """Deletes the contents of the public directory"""
    shutil.rmtree(public)
    os.mkdir(public)


def get_static_assets(static_dir: str, public_dir: str) -> None:
    """Clears the public directory, then copies all assets from the static director to the public directory."""
    if not (isinstance(static_dir, str) and isinstance(public_dir, str)):
        raise TypeError

    # if not (os.path.exists(static_dir) and os.path.exists(public_dir)):
    #     raise ValueError
    os.makedirs(static_dir, exist_ok=True)
    os.makedirs(public_dir, exist_ok=True)
    if not (os.path.isdir(static_dir) and os.path.isdir(public_dir)):
        raise NotADirectoryError

    visited: set = set()
    static: str = os.path.abspath(static_dir)
    public: str = os.path.abspath(public_dir)
    _reset_public(public)
    dfs_visit(public, static, visited)


def dfs_visit(dest_dir: str, source_dir: str, visited: set):
    stack: list[str] = []
    visited.add(source_dir)
    files = os.listdir(source_dir)
    for file in files:
        file_path = os.path.join(source_dir, file)
        if not os.path.isfile(file_path):
            stack.append(file)
        else:
            shutil.copy(file_path, dest_dir)

    while len(stack) > 0:
        dir = stack.pop()
        pub = os.path.join(dest_dir, dir)
        if not os.path.exists(pub):
            os.mkdir(pub)
        stat = os.path.join(source_dir, dir)
        dfs_visit(pub, stat, visited)


if __name__ == "__main__":
    static = "static"
    public = "public"
    get_static_assets(static, public)
