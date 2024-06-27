import re


def token(typ):
    def action(scanner, token):
        return typ, token
    return action


scanner = re.Scanner([
    (r'\s+', None),
    (r'\w+', token('NAME')),
    (r'#.*', token('MACRO')),
    (r'//.*|/\*[\s\S]*?\*/', token('COMMENT')),
    (r'"[^"]*"', token('STRING')),
    ('[%s]' % re.escape(',;()[]{}'), token('SEPRATOR')),
    ('[%s]+' % re.escape('+-*/%<=>|&!?:'), token('OPERATOR')),
])


def Parse(text):
    results, remainder = scanner.scan(text)
    assert remainder == '', repr(remainder[:50])

    for typ, name in results:
        print(f'{typ:>9}: {name}')


def ParseFile(file):
    try:
        with open(file, encoding='u8') as f:
            text = f.read()
    except UnicodeError:
        with open(file) as f:
            text = f.read()
    Parse(text)


if __name__ == '__main__':
    ParseFile('test.c')
