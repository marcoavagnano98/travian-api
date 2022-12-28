def get_key_from_value(dict, value):
    keys = [k for k, v in dict.items() if v == value]
    return keys[0] if len(keys) > 0 else ''


def check_key(dict, key, default):
    return key in dict or key == default
