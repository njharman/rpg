# vim: set fileencoding=utf-8 name> :
'''
Stuff to parse rpg pdf's  converted to text
'''
import re
import sys

from rst import TITLES

PAGE_BREAK = '\f'

re_emptyline = re.compile(r'^\s*$')

# Sort alphabetically 10 after 2,4,8,etc.
alpha_sort = lambda key: [int(t) if t.isdigit() else t for t in re.split('([0-9]+)', key)]


def replace(lines):
    '''Replace weirdo characters.'''
    for line in lines:
        yield line.replace('“', '"').replace('”', '"').replace('—', '--').replace('’', '\'').replace('\xe2\x80\x93', '-')


def strip_newlines(lines, strip='\n'):
    '''Strip newlines from end of lines.'''
    for line in lines:
        yield line.strip(strip)


def strip_empty(lines):
    '''Remove lines containing only whitespace.'''
    for line in lines:
        if line.strip():
            yield line


def strip_comments(lines):
    '''## indicates comment line'''
    for line in lines:
        if not line.startswith('##'):
            yield line


def strip_tt_pagebreaks(lines):
    '''TT has pagenumber preceding pagebreak'''
    previous = None
    for line in lines:
        if PAGE_BREAK in line:
            line.replace(PAGE_BREAK, '')
            previous = None
        if previous is not None:
            yield previous
        previous = line
    if previous:
        yield previous


def strip_aec_pagebreaks(lines):
    '''AEC has pagenumber after pagebreak and page break line is garbage'''
    skip = False
    for line in lines:
        if PAGE_BREAK in line:
            skip = True
            continue
        if skip:
            skip = False
            continue
        yield line


def split_on_pagebreak(lines):
    '''Split lines on page break char ^L.'''
    page = list()
    for l in lines:
        if PAGE_BREAK in l:
            page.pop()  # the pagenumber/footer
            yield page
            page = list()
            page.append(l.replace(PAGE_BREAK, '').strip('\n'))
        else:
            page.append(l)


def dehypenate(lines):
    '''Combine two lines with hypenated word into one line, removing hypen.'''
    first = ''
    for line in lines:
        line = line.rstrip()
        if len(line) > 1 and line[-1] == '-' and line[-2] != '-':
            first += line[:-1]
            continue
        yield first + line
        first = ''


def by_para(lines, tests=()):
    '''Splits into para happen on
      - blank lines
      - lines ending with .
      - lines ending with : (if only one colon on line)
    Understand ReST orders, titles and tables. marks them with <order>, <title> <table>
    Dehyphenates.
    :return: single line (with possible newlines embedded (for tables))
    '''
    def break_base(line, accum):
        # Break on blank line or after line ending with period or colon (if only colon on line)
        if not line or line.endswith('.') or (line.endswith(':') and line.count(':') == 1):
            if line:
                accum.append(line)
            return True
    def break_list(line, accum):
        # Break before "List Header:" should be on its own line.
        if accum and line.endswith(':') and line.count(':') == 1 and is_cap(line[0]):
            return line
    tests = list(tests)
    tests.append(break_base)
    tests.append(break_list)
    in_table = 0
    in_order = 0
    accumulate = list()
    for line in lines:
        # ReST directive. Must be first, sucks all lines until unindent.
        if line.startswith('.. '):
            yield ' '.join(accumulate)
            accumulate = list()
            line = '<order>' + line
            in_order = True
        if in_order:
            if line.startswith(' ') or not line:
                accumulate.append(line)
                continue
            else:
                in_order = False
                yield '\n'.join(accumulate)
                accumulate = list()

        # ReST title
        if line and line[0] in TITLES and len(accumulate) == 1 and len(accumulate[0]) == len(line):
            yield '<title>%s\n%s' % (accumulate[0], line)
            accumulate = list()
            continue

        # ReST table
        if line.startswith('==='):
            if in_table == 0:  # End previous para, start table.
                yield ' '.join(accumulate)
                line = '<table>' + line
                accumulate = list()
            if in_table < 2:  # Tables, have three === seperator lines.
                in_table += 1
            else:  # End table.
                in_table = 0
                accumulate.append(line.rstrip())
                yield '\n'.join(accumulate)
                accumulate = list()
                continue
        if in_table:
            accumulate.append(line.rstrip())
            continue

        for test in tests:
            foo = test(line, accumulate)
            if foo:
                yield ' '.join(dehypenate(accumulate))
                accumulate = list()
                if foo is not True:
                    accumulate.append(foo)
                break
        else:
            accumulate.append(line)

    # TODO: might need '\n'.join
    if accumulate:
        yield ' '.join(dehypenate(accumulate))


def slurp_re(stopon, i, lines, strip):
    '''Slurp lines until line matches re 'stopon'.'''
    bits = list()
    bits.append(lines[i].rpartition(strip)[2].strip())
    while not stopon.match(lines[i + 1]):
        i += 1
        bits.append(lines[i].strip())
    return i, ' '.join(bits).strip()


def lookfor(test, accum, reduce):
    def finder(line):
        accum.append(line)
        try:
            if test(line):
                for para in reduce(accum):
                    yield para
        except Exception as e:
            print >> sys.stderr, '\n'.join(line)
            raise
    return finder


def is_cap(char):
    '''lookfor test'''
    return char == char.upper()


def space_reduce(lines):
    '''lookfor reducer'''
    yield ' '.join(lines)
