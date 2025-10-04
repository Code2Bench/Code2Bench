

def parse_hp_string(hp_string):
    result = {}
    for pair in hp_string.split(','):
        if not pair:
            continue
        key, value = pair.split('=')
        try:
            # 自动转换为 int / float / str
            ori_value = value
            value = float(value)
            if '.' not in str(ori_value):
                value = int(value)
        except ValueError:
            pass

        if value in ['true', 'True']:
            value = True
        if value in ['false', 'False']:
            value = False
        if '.' in key:
            keys = key.split('.')
            keys = keys
            current = result
            for key in keys[:-1]:
                if key not in current or not isinstance(current[key], dict):
                    current[key] = {}
                current = current[key]
            current[keys[-1]] = value
        else:
            result[key.strip()] = value
    return result