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


def Token(typ):
    def action(scanner, token):
        return typ, token
    return action


def Parse(text):
    scanner = re.Scanner([(patt, Token(typ)) for typ, patt in token_patts.items()])
    results, remainder = scanner.scan(text)
    assert remainder == '', repr(remainder[:50])

    for typ, name in results:
        if typ != 'SPACE':
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
