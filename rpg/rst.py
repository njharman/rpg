'''
ReStructuredText tools
'''
import textwrap

TITLES = ['*', '=', '-', '~']


indenter = textwrap.TextWrapper(subsequent_indent='  ').fill


def parapper(text):
    # Don't rap with embeded newlines.
    if '\n' in text:
        return text
    return textwrap.TextWrapper().fill(text)


def title(level, text):
    if level not in TITLES:
        level = TITLES[int(level)]
    return '\n%s\n%s' % (text, level * len(text))


def page(style):
    return '\n.. page:: %s\n' % style


def print_paragraphs(seq):
    print
    print '\n\n'.join(seq)


def escape_asterisk(text):
    '''Asterisks are strong/emphasis in ReST.'''
    return text.replace('*', '\*')
