import os
import re


token_patts = {
    'SPACE': r'\s+',
    'NAME': r'\w+',
    'MACRO': r'#.*',
    'COMMENT': r'//.*|/\*[\s\S]*?\*/',
    'STRING': r'"[^"]*"',
    'SEPRATOR': '[%s]' % re.escape(',;()[]{}'),
    'OPERATOR': '[%s]+' % re.escape('+-*/%<=>|&!?:'),
}


class Node:
    def __init__(self, parent=None, value='root'):
        self.parent = parent
        self.value = value
        self.children = []
        if parent is not None:
            parent.children.append(self)

    def __getitem__(self, item):
        if isinstance(item, tuple):
            for key in item:
                self = self[key]
            return self
        if isinstance(item, type(...)):
            return self.parent
        if isinstance(item, int):
            return self.children[item]
        raise TypeError(type(item))

    def __iter__(self):
        yield from self.children

    def __len__(self):
        return len(self.children)

    def __repr__(self):
        return f'Node({self.value!r})'

    def __str__(self):
        return f'{self.value}'

    def iter(self, lv=0, id=0):
        yield lv, id, self
        for id, child in enumerate(self):
             yield from child.iter(lv + 1)

    def show(self):
        lines = [lv * '  ' + f'{node}\n' for lv, id, node in self.iter()]
        print(''.join(lines))


def Token(typ):
    def action(scanner, token):
        return typ, token
    return action


def ParseText(text):
    scanner = re.Scanner([(patt, Token(typ)) for typ, patt in token_patts.items()])
    results, remainder = scanner.scan(text)
    assert remainder == '', repr(remainder[:50])

    node = root = Node()
    for typ, name in results:
        if typ == 'SPACE':
            pass
        elif typ == 'SEPRATOR':
            if name in '([{':
                node = Node(node, name)
            elif name in '}])':
                node = node.parent
                Node(node, name)
            else:
                Node(node, name)
        else:
            Node(node, name)

    return root


def ParseFile(file):
    try:
        with open(file, encoding='u8') as f:
            text = f.read()
    except UnicodeError:
        with open(file) as f:
            text = f.read()
    return ParseText(text)


def Parse(file_or_text):
    if os.path.isfile(file_or_text):
        return ParseFile(file_or_text)
    else:
        return ParseText(file_or_text)


if __name__ == '__main__':
    root = Parse('test.c')
    root.show()

    text = "int main(int argc, char* argv[]) { int a = 1; int b = 2; return a + b; }"
    root = Parse(text)
    root.show()
