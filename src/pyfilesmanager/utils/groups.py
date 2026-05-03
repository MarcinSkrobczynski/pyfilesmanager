from collections import defaultdict
from collections.abc import Callable, Iterable

NUMBER_OF_GROUP_BY_THRESHOLD = 2


def group_by[T, K](items: Iterable[T], key_fn: Callable[[T], K]) -> dict[K, list[T]]:
    groups: defaultdict[K, list[T]] = defaultdict(list)
    for item in items:
        groups[key_fn(item)].append(item)
    return {k: v for k, v in groups.items() if len(v) >= NUMBER_OF_GROUP_BY_THRESHOLD}
