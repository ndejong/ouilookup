import ouilookup


def test_name_exist():
    assert ouilookup.__name__ is not None


def test_version_exist():
    assert ouilookup.__version__ is not None
