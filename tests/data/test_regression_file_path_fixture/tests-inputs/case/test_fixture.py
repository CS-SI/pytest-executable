from fnmatch import fnmatch


def test_fixture(regression_file_path):
    assert fnmatch(str(regression_file_path.relative), "[01].xmf")
    assert fnmatch(
        str(regression_file_path.absolute),
        "*/test_regression_file_path_fixture0/references/case/[01].xmf",
    )
