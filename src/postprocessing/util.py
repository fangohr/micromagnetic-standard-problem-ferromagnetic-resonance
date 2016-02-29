def convert_to_unit(val, unit):
    """
    Convert the timestep value(s) `val` from seconds to `unit`, which may
    either be "s" (= seconds), in which case `val` is returned unchanged,
    or "ns" (= nanoseconds).
    """
    if unit == 's':
        return val
    elif unit == 'ns':
        return val * 1e9
    else:
        msg = ("The argument `unit` must be either 's' (= seconds) "
               "or 'ns' (= nanoseconds). Got: '{}'".format(unit))
        raise ValueError(msg)


def get_index_of_m_avg_component(component):
    """
    Internal helper function to return the column index for the x/y/z
    component of the average magnetisation. Note that indices start at
    1, not zero, because the first column contains the timesteps.
    (TODO: This may be different for other data types, though!)
    """
    try:
        idx = {'x': 1, 'y': 2, 'z': 3}[component]
    except KeyError:
        raise ValueError(
            "Argument 'component' must be one of 'x', 'y', 'z'. "
            "Got: '{}'".format(component))
    return idx
