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
    def __init__(self, parent=None, data=None):
        self.parent = parent
        self.data = data
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
        return f'Node({self.data!r})'

    def __str__(self):
        return f'{self.data}'

    def iter(self, lv=0, id=0):
        yield lv, id, self
        for id, child in enumerate(self):
             yield from child.iter(lv + 1)

    def show(self):
        lines = [lv * '  ' + f'{node}\n' for lv, id, node in self.iter()]
        print(''.join(lines))


PREFIX_NONE = 0
PREFIX_SPACE = 1
PREFIX_INDENT = 2


class CNode(Node):
    def __init__(self, parent=None, value='root', prefix=PREFIX_INDENT):
        Node.__init__(self, parent, (value, prefix))

    def show(self):
        results = []
        for lv, id, node in self.iter():
            value, prefix = node.data
            if prefix == PREFIX_NONE:
                prefix = ''
            elif prefix == PREFIX_SPACE:
                prefix = ' '
            elif prefix == PREFIX_INDENT:
                prefix = '\n' + '  ' * lv
            results.append(f'{prefix}{value}')
        print(''.join(results))


def Token(typ):
    def action(scanner, token):
        return typ, token
    return action


def ParseText(text):
    scanner = re.Scanner([(patt, Token(typ)) for typ, patt in token_patts.items()])
    results, remainder = scanner.scan(text)
    assert remainder == '', repr(remainder[:50])

    node = root = CNode()
    prefix_next = PREFIX_INDENT
    for typ, name in results:
        if typ == 'SPACE':
            pass
        elif typ == 'SEPRATOR':
            if name in '([{':
                node = CNode(node, name, PREFIX_SPACE)
                prefix_next = PREFIX_INDENT
            elif name in '}])':
                prefix = PREFIX_NONE if len(node) == 0 else PREFIX_INDENT
                node = node.parent
                CNode(node, name, prefix)
                prefix_next = PREFIX_INDENT if name == '}' else PREFIX_SPACE
            elif name in ',;':
                CNode(node, name, PREFIX_NONE)
                prefix_next = PREFIX_INDENT
            else:
                raise ValueError(repr(name))
        elif typ in ['MACRO', 'COMMENT']:
            CNode(node, name, PREFIX_INDENT)
            prefix_next = PREFIX_INDENT
        else:
            CNode(node, name, prefix_next)
            prefix_next = PREFIX_SPACE

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
