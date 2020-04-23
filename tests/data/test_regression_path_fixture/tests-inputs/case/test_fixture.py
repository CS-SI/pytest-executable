from fnmatch import fnmatch


def test_fixture(regression_path):
    assert fnmatch(
        str(regression_path), "*/test_regression_path_fixture0/references/case"
    )
