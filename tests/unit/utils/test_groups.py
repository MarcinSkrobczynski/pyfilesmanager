from pyfilesmanager.utils.groups import group_by


def test_group_by_empty():
    assert group_by([], lambda x: x) == {}


def test_group_by_no_groups():
    assert group_by([1, 2, 3], lambda x: x) == {}


def test_group_by_returns_groups():
    assert group_by([1, 2, 3, 3], lambda x: x) == {3: [3, 3]}


def test_group_by_multiple_groups():
    assert group_by([1, 1, 2, 2, 3], lambda x: x) == {1: [1, 1], 2: [2, 2]}
