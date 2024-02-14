
def to_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

def convert_keys(data):
    if isinstance(data, dict):
        new_dict = {}
        for key, value in data.items():
            new_key = to_camel_case(key)
            new_dict[new_key] = convert_keys(value)
        return new_dict
    elif isinstance(data, list):
        return [convert_keys(item) for item in data]
    else:
        return data
