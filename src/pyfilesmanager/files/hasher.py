import hashlib
import pathlib


def compute_hash(filepath: pathlib.Path, bytes_limit: int | None = None, chunk_size: int = 65536) -> str:
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        if bytes_limit is None:
            while chunk := f.read(chunk_size):
                hasher.update(chunk)
        else:
            remaining = bytes_limit
            while remaining > 0:
                chunk = f.read(min(chunk_size, remaining))
                if not chunk:
                    break
                hasher.update(chunk)
                remaining -= len(chunk)
    return hasher.hexdigest()
