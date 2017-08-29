'''ReStructuredText output tools
'''
from functools import wraps


TITLES = ['*', '=', '-', '~']


def page(style):
    '''Page break.'''
    return '\n.. page:: %s\n' % style


def escape_asterisk(text):
    '''Asterisks are strong/emphasis in ReST.'''
    return text.replace('*', '\*')


def title(level, text):
    if level not in TITLES:
        level = TITLES[int(level)]
    return '\n%s\n%s' % (text, level * len(text))


def title_by_regex(lines, regexes, level):
    '''ReST Title lines matching regex.'''
    for l in lines:
        if [r for r in regexes if r.search(l)]:
            yield ''
            yield l
            yield level * len(l)
        else:
            yield l


def TitleByRegexFactory(regexes, level='='):
    try:
        iter(regexes)
    except TypeError:
        regexes = [regexes, ]

    @wraps(title_by_regex)
    def inner(lines):
        return title_by_regex(lines, regexes, level)
    return inner
