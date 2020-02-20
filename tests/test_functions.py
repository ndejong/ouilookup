
import pytest
import OuiLookup


def test_OuiLookup_query():
    OL = OuiLookup.OuiLookup()
    data = OL.query('00:00:aa:00:00:00')

    assert type(data) is list
    assert len(data) == 1
    assert type(data[0]) is dict
    assert '0000AA000000' in data[0]
    assert data[0]['0000AA000000'] == 'XEROX CORPORATION'


def test_OuiLookup_query_multi():
    OL = OuiLookup.OuiLookup()
    data = OL.query('00:00:01:00:00:00 00-00-10-00-00-00 000011000000')

    assert type(data) is list
    assert len(data) == 3
    assert '000001000000' in data[0]
    assert '000010000000' in data[1]
    assert '000011000000' in data[2]
    assert data[0]['000001000000'] == 'XEROX CORPORATION'
    assert data[1]['000010000000'] == 'SYTEK INC.'
    assert data[2]['000011000000'] == 'NORMEREL SYSTEMES'


def test_OuiLookup_status():
    OL = OuiLookup.OuiLookup()
    data = OL.status()

    assert type(data) is dict
    assert 'data_file' in data
    assert 'data_path' in data
    assert 'source_bytes' in data
