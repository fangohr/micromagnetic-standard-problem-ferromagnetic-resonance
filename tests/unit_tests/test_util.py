from postprocessing.util import get_conversion_factor


def test__get_conversion_factor():
    assert get_conversion_factor('s', 's') == 1.0
    assert get_conversion_factor('s', 'ns') == 1e9
    assert get_conversion_factor('ns', 's') == 1e-9
    assert get_conversion_factor('ns', 'ns') == 1.0

    assert get_conversion_factor('Hz', 'Hz') == 1.0
    assert get_conversion_factor('Hz', 'GHz') == 1e-9
    assert get_conversion_factor('GHz', 'Hz') == 1e9
    assert get_conversion_factor('GHz', 'GHz') == 1.0
