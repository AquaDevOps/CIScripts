def simple_value(val):
    return ('"%s"' if isinstance(val, str) else '%s') % val

