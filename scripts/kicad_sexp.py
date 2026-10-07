import re


def parse(text):
    stack = []
    for token in re.findall(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+', text):
        if token == "(":
            stack.append([])
        elif token == ")":
            node = stack.pop()
            if not stack:
                return node
            stack[-1].append(node)
        else:
            stack[-1].append(token.strip('"'))
    raise ValueError("Incomplete KiCad expression")


def children(node, kind):
    return [item for item in node if isinstance(item, list) and item[0] == kind]


def child(node, kind):
    return next(iter(children(node, kind)), None)
