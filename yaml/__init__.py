import re

def safe_load(stream):
    text = stream.read() if hasattr(stream, 'read') else str(stream)
    data = {}
    stack = [data]
    indents = [0]
    for raw in text.splitlines():
        line = raw.split('#',1)[0].rstrip()
        if not line.strip():
            continue
        indent = len(raw) - len(raw.lstrip(' '))
        key, _, value = line.lstrip().partition(':')
        key = key.strip()
        value = value.strip()
        while indents and indent < indents[-1]:
            stack.pop()
            indents.pop()
        cur = stack[-1]
        if value == '':
            cur[key] = {}
            stack.append(cur[key])
            indents.append(indent + 2)
            continue
        if value.startswith('[') and value.endswith(']'):
            items = [v.strip().strip('"\'') for v in value[1:-1].split(',') if v.strip()]
            cur[key] = items
        else:
            if value.isdigit():
                cur[key] = int(value)
            elif (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
                cur[key] = value[1:-1]
            else:
                cur[key] = value
    return data
