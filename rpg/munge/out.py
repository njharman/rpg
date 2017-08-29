## Output
import textwrap

indenter = textwrap.TextWrapper(subsequent_indent='  ').fill


def parapper(text):
    '''Wrap lines.'''
    # Don't rap with embeded newlines.
    if '\n' in text:
        return text
    return textwrap.TextWrapper().fill(text)


def paragraphs(seq):
    return '\n\n'.join(seq)
