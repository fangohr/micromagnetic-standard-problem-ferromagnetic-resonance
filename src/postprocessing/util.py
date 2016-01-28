def get_conversion_factor(from_unit, to_unit):
    """
    Return the conversion factor which converts a value given in unit
    `from_unit` to a value given in unit `to_unit`.

    Allowed values for `from_unit`, `to_unit` are 's' (= second), 'ns'
    (= nanosecond), 'Hz' (= Hertz) and 'GHz' (= GigaHertz). An error
    is raised if a different unit is given.

    Example:

       >>> get_conversion_factor('s', 'ns')
       1e9

    """
    allowed_units = ['s', 'ns', 'Hz', 'GHz']
    if not set([from_unit, to_unit]).issubset(allowed_units):
        raise ValueError("Invalid unit: '{}'. Must be one of " + ", ".join(allowed_units))

    return {('s', 's'): 1.0,
            ('s', 'ns'): 1e9,
            ('ns', 's'): 1e-9,
            ('ns', 'ns'): 1.0,
            ('Hz', 'Hz'): 1.0,
            ('Hz', 'GHz'): 1e-9,
            ('GHz', 'Hz'): 1e9,
            ('GHz', 'GHz'): 1.0}[(from_unit, to_unit)]


def get_index_of_m_avg_component(component):
    """
    Internal helper function to return the column index for the x/y/z component
    of the average magnetisation. Note that indices start at 1, not zero,
    because the first column contains the timesteps.

    (TODO: This may be different for other data types, though!)

    """
    try:
        idx = {'x': 1, 'y': 2, 'z': 3}[component]
    except KeyError:
        raise ValueError(
            "Argument 'component' must be one of 'x', 'y', 'z'. "
            "Got: '{}'".format(component))
    return idx
