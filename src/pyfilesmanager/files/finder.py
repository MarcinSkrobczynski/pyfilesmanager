import pathlib
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

import click

from pyfilesmanager.files.hasher import compute_hash
from pyfilesmanager.files.scanner import collect_valid_files
from pyfilesmanager.utils.groups import group_by

PARTIAL_HASH_BYTES = 4096
NUMBER_OF_HASH_CANDIDATES_THRESHOLD = 2


def _hash_candidates(
    paths: list[pathlib.Path],
    label: str,
    bytes_limit: int | None = None,
) -> tuple[dict[str, list[pathlib.Path]], list[tuple[pathlib.Path, OSError]]]:
    hashes: defaultdict[str, list[pathlib.Path]] = defaultdict(list)
    failures: list[tuple[pathlib.Path, OSError]] = []

    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(compute_hash, path, bytes_limit): path for path in paths}
        with click.progressbar(length=len(paths), label=label) as bar:
            for future in as_completed(futures):
                path = futures[future]
                try:
                    hashes[future.result()].append(path)
                except OSError as e:
                    failures.append((path, e))
                bar.update(1)

    return {h: ps for h, ps in hashes.items() if len(ps) >= NUMBER_OF_HASH_CANDIDATES_THRESHOLD}, failures


def _write_debug_files(duplicates: dict[str, list[pathlib.Path]], output_dir: pathlib.Path) -> None:
    with open(output_dir / "duplicates.txt", "w") as f:
        for file_hash, paths in duplicates.items():
            f.write(f"{file_hash} => {[str(p) for p in paths]}\n")


def find_duplicate_files(dir_path: pathlib.Path, **kwargs) -> dict[str, list[pathlib.Path]]:
    debug = kwargs.get("debug", False)
    output_dir = kwargs.get("output_dir", pathlib.Path("."))

    # Stage 1: group by size (stat only, no file reads)
    by_size = group_by(collect_valid_files(dir_path), lambda p: p.stat().st_size)
    size_candidates = [p for paths in by_size.values() for p in paths]

    if debug:
        click.echo(f"Stage 1: {len(size_candidates)} candidates after size filter")

    if not size_candidates:
        return {}

    # Stage 2: partial hash (first 4 KB)
    by_partial, failures = _hash_candidates(size_candidates, "Scanning (partial)...", bytes_limit=PARTIAL_HASH_BYTES)
    partial_candidates = [p for paths in by_partial.values() for p in paths]

    if debug:
        click.echo(f"Stage 2: {len(partial_candidates)} candidates after partial hash")

    # Stage 3: full hash
    duplicates, more_failures = _hash_candidates(partial_candidates, "Scanning (full)...")
    failures.extend(more_failures)

    for path, err in failures:
        click.secho(f"Failed to hash {path}: {err}", fg="red", err=True)

    if debug:
        _write_debug_files(duplicates, output_dir)

    return duplicates
