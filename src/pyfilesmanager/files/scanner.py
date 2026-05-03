import os
import pathlib


def collect_valid_files(dir_path: pathlib.Path) -> list[pathlib.Path]:
    files = []
    for root, _, filenames in os.walk(dir_path):
        for filename in filenames:
            path = pathlib.Path(root) / filename
            if not path.is_symlink() and path.stat().st_size > 0:
                files.append(path)
    return files
