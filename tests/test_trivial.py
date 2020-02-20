
import pytest
import OuiLookup

def test_name_exist():
    ol = OuiLookup
    assert ol.NAME is not None


def test_version_exist():
    ol = OuiLookup
    assert ol.VERSION is not None
